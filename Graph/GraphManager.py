import sys, re,urllib,requests, codecs, operator, gzip, timeit, io
from bs4 import BeautifulSoup, NavigableString
from Graph.TopicNode import TopicNode
from Graph.Topic import Topic
from BSHelpers.WebTool import WebTool
from BSHelpers.SourceElement import SourceElement
from FileWriters.GraphWriter import GraphWriter
import pickle, dill, logging
from functools import partial
from itertools import repeat, chain
from multiprocessing import Pool, cpu_count, Manager
from multiprocessing.managers import BaseManager

import nltk


logging.basicConfig(level=logging.DEBUG)

class GraphManager:



	def __init__(self):
		self.nodes = {}
		self.populatedNodes = {};
		self.tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

	def saveGraph(self, name):
		logging.info("Saving graph...", end ='')
		GraphWriter.writeGraph(self.nodes, 'GraphData/LGF/'+ name + '_graphData.lgf')
		pickle.dump(self.nodes, open('GraphData/P/'+ name +'_graphNodes.p', "wb"))
		logging.info("Save complete!")

	def readGraph(self, name):
		logging.info("Reading in graph... ", end='')
		self.nodes = pickle.load(open("GraphData/P/" + name + "_graphNodes.p", "rb"))
		logging.info("Loaded successfully")

	def p_dive(self):
		#tmp = self.nodes
		pool = Pool(cpu_count() *2)
		for item in list(self.nodes.keys()):
			cons = list(self.nodes[item].getConnections().values())
			logging.debug('waiting')
			nodesPopulated = pool.map(self.populateTopicNode, cons)
			logging.debug('Home!')

			logging.debug('finished diving')
			for node in nodesPopulated:
				if(node != None):
					self.nodes[node.getTopic().getName()] = node
					self.populatedNodes[node.getTopic().getName()] = True;
		pool.close()
		pool.join()


	def p_beginSearch(self, startingNode, depth, save = False, poolChunkSize = 0):

		#pool = Pool(cpu_count() * 2)
		current_depth = 1
		#pool.map(self.populateTopicNode, [startingNode])
		self.nodes[startingNode.getTopic().getName()] = startingNode
		startingNode = self.populateTopicNode('1.'+startingNode.getTopic().getName())
		if save:
			logging.debug('saving 1 deep')
			self.saveGraph('p1')
		if depth == 1:
			return

		currentNode = startingNode
		nodesPopulated = [currentNode]
		connections = []
		merger = []
		pool = Pool(cpu_count()+2)
		logging.debug()
		logging.debug('=' * 70)
		for currentDepth in range(1, depth):

			logging.debug("=  At depth %" % currentDepth)
			connections = []
			logging.debug('=  Successfully populated another round of nodes\n')
			for item in nodesPopulated:
				if item != None:
					self.nodes[item.getTopic().getName()] = item
					for otherItem in list(item.getConnections().values()):
						if otherItem != None and otherItem.isPopulated() == False:
							topicName = otherItem.getTopic().getName()
							self.nodes[topicName] = otherItem
							connections.append(str(currentDepth+1) + '.'+topicName)

			logging.debug("=  Current number of connections: %s" % len(connections))
			logging.debug("=  Current number of NodesPopulated in this iteration: %s" % len(nodesPopulated))
			logging.debug("=  Total number of nodes %" % len(self.nodes.keys()))


			if poolChunkSize <= 0:
				nodesPopulated = pool.map_async(self.populateTopicNode, connections)
			else:
				nodesPopulated = pool.map_async(self.populateTopicNode, connections, poolChunkSize)
			nodesPopulated.wait()
			nodesPopulated = nodesPopulated.get()
			logging.debug('=  Updated self.nodes\n % s' % '='*70)
			if save and currentDepth+1 != depth:
				logging.debug('saving %s %s' % currentDepth, 'deep')
				val = str(currentDepth)
				self.saveGraph('p'+val)


		pool.close()
		pool.join()

		for item in nodesPopulated:
			if item != None:
				self.nodes[item.getTopic().getName()] = item
		if save:
			logging.debug("last save")
			val = str(currentDepth+1)
			self.saveGraph('p' + val)

		logging.debug('\nCount = ',len(list(self.nodes.keys())))
		return

	def populateTopicNode(self, key):
		spot = key.find('.')
		depth = key[:spot]
		key = key[spot+1:]

		node = self.nodes[key]
		if node.getDepthFound() == 0:
			node.setDepthFound(depth)
		keyxyz = node.getTopic().getName()
		if(node.isPopulated()):
			logging.warning(node.getTopic(), 'ERROR1')
			return None
		sourceCode = WebTool.getValidatedTopicSourceCode(node.getTopic().getName())
		if sourceCode == None:
			logging.warning(node.getTopic(), 'ERROR2')
			return None
		sourceElement = SourceElement(sourceCode)
		sourceElement.validateName(node)
		if(node.isPopulated()):
			logging.warning(node.getTopic(), 'ERROR3')
			return None

		links = sourceElement.grabIntroAndSeeAlsoLinks(node)
		logging.debug('%s %s' % (node.getTopic(), '|'))
		self.addInfoToNewNodes(node, links)
		node.setCategory(sourceElement.getCategories())
		node.setIsPopulated()
		self.createConnectionDetails(node)
		logging.debug()
		if dill.pickles(node):
			return node
		else:
			logging.debug( dill.detect.badtypes(node, depth=1).keys())
			logging.critical(node.getTopic(), 'Failed pickle')
			return None

	def addInfoToNewNodes(self, node, links):
		count = 0
		for link in list(links.keys()):
			nextTopic = Topic(link)
			nextTopicNode = TopicNode(nextTopic)
			SourceElement.staticValidateName(nextTopicNode)
			try:
				SourceElement.staticValidation(nextTopicNode)
			except Exception as e:
				logging.debug("ERROR IN STATIC EVAL:\n", e)
				continue
			if(self.isBadLink(nextTopicNode)):
				continue
			#node.setDetailingName(nextTopic, links[link])
			node.setDetailingName(nextTopic, links[link])
			node.addConnection(nextTopicNode);
			count += 1

		logging.debug('.'*count)



	def createConnectionDetails(self, node):
		data = re.sub('\(([^\)]+)\)', '',node.getIntroText())
		tokenized = self.tokenizer.tokenize(data)
		for con in node.getConnections().keys():
			name = re.escape(node.getDetailingName(con))
			for sentence in tokenized:
				if name in sentence or node.getDetailingName(con) in sentence:
					node.addConnectionDetail(con, sentence)
					break



	def isBadLink(self, topicNode):
		name = topicNode.getTopic().getName()
		n = any(re.findall('List of|Wikipedia|File:', name, re.IGNORECASE))
		if n:
			logging.debug('(N)',  end='')
			return True
		#check categories
		catCheck = 'portal:|list |lists |wikipedia|file|help|template|category:'
		categories = topicNode.getCategories()
		for cat in categories:
			c =  any(re.findall(catCheck, cat, re.IGNORECASE))
			if c:
				logging.debug('(C)', end='')
				return True

		return False

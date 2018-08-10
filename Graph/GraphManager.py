import sys, re,urllib,requests, codecs, operator, gzip, timeit, io
from bs4 import BeautifulSoup, NavigableString
from Graph.TopicNode import TopicNode
from Graph.Topic import Topic
from BSHelpers.WebTool import WebTool
from BSHelpers.SourceElement import SourceElement
from FileWriters.GraphWriter import GraphWriter
import pickle, dill
from functools import partial
from itertools import repeat, chain
from multiprocessing import Pool, cpu_count, Manager
from multiprocessing.managers import BaseManager

import nltk

class GraphManager:



	def __init__(self):
		self.nodes = {}
		self.populatedNodes = {};
		self.tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

	def saveGraph(self, name):
		print("Saving graph...", end ='')
		GraphWriter.writeGraph(self.nodes, 'GraphData/'+ name + '_graphData.lgf')
		pickle.dump(self.nodes, open('GraphData/'+ name +'_graphNodes.p', "wb"))
		print("Save complete!")

	def readGraph(self, name):
		print("Reading in graph... ", end='')
		self.nodes = pickle.load(open("GraphData/" + name + "_graphNodes.p", "rb"))
		print("Loaded successfully")

	def p_dive(self):
		#tmp = self.nodes
		pool = Pool(cpu_count() *2)
		for item in list(self.nodes.keys()):
			cons = list(self.nodes[item].getConnections().values())
			print('waiting')
			nodesPopulated = pool.map(self.populateTopicNode, cons)
			print('Home!')

			print('finished diving')
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
		#if save:
			#self.saveGraph('p1')
		if depth == 1:
			return

		currentNode = startingNode
		nodesPopulated = [currentNode]
		connections = []
		merger = []
		pool = Pool(cpu_count()+2)
		#print()
		#print('=' * 70)
		for currentDepth in range(1, depth):

			#print("=  At depth", currentDepth)
			connections = []
			#print('=  Successfully populated another round of nodes\n')
			for item in nodesPopulated:
				if item != None:
					self.nodes[item.getTopic().getName()] = item
					for otherItem in list(item.getConnections().values()):
						if otherItem != None and otherItem.isPopulated() == False:
							topicName = otherItem.getTopic().getName()
							self.nodes[topicName] = otherItem
							connections.append(str(currentDepth+1) + '.'+topicName)
				#if save and currentDepth != depth:
					#val = str(currentDepth)
					#self.saveGraph('p'+val)
			#print("=  Current number of connections:",len(connections))
			#print("=  Current number of NodesPopulated in this iteration: ",len(nodesPopulated))
			#print("=  Total number of nodes",len(self.nodes.keys()))
			if poolChunkSize <= 0:
				nodesPopulated = pool.map_async(self.populateTopicNode, connections)
			else:
				nodesPopulated = pool.map_async(self.populateTopicNode, connections, poolChunkSize)
			nodesPopulated.wait()
			nodesPopulated = nodesPopulated.get()
			#print('=  Updated self.nodes\n', '='*70)


		pool.close()
		pool.join()

		for item in nodesPopulated:
			if item != None:
				self.nodes[item.getTopic().getName()] = item
		#if save:
			#val = str(currentDepth+1)
			#self.saveGraph('p' + val)
		#print('\nCount = ',len(list(self.nodes.keys())))
		return

	def populateTopicNode(self, key):
		spot = key.find('.')
		depth = key[:spot]
		key = key[spot+1:]

		node = self.nodes[key]
		if node.getDepthFound() == 0:
			node.setDepthFound(depth)
		keyxyz = node.getTopic().getName()
		#print("3.",end='')
		if(node.isPopulated()):
			print("Populated!")
			return None
		sourceCode = WebTool.getValidatedTopicSourceCode(node.getTopic().getName())
		if sourceCode == None:
			#print('fuck off')
			return None
		sourceElement = SourceElement(sourceCode)
		sourceElement.validateName(node)
		if(node.isPopulated()):
			return None

		links = sourceElement.grabIntroAndSeeAlsoLinks(node)
		#print(node.getTopic(), '|', end='')
		self.addInfoToNewNodes(node, links)
		node.setCategory(sourceElement.getCategories())
		node.setIsPopulated()
		self.createConnectionDetails(node)
		#print()
		if dill.pickles(node):
			return node
		else:
			print( dill.detect.badtypes(node, depth=1).keys())
			quit()
			return None

	def addInfoToNewNodes(self, node, links):
		for link in list(links.keys()):
			nextTopic = Topic(link)
			nextTopicNode = TopicNode(nextTopic)
			SourceElement.staticValidateName(nextTopicNode)
			try:
				SourceElement.staticValidation(nextTopicNode)
			except Exception as e:
				print("ERROR IN STATIC EVAL:\n", e)
				continue
			if(self.isBadLink(nextTopicNode)):
				continue
			#node.setDetailingName(nextTopic, links[link])
			node.setDetailingName(nextTopic, links[link])
			node.addConnection(nextTopicNode);
			#print('.', end='')



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
			print('(N)',  end='')
			return True
		#check categories
		catCheck = 'portal:|list |lists |wikipedia|file|help|template|category:'
		categories = topicNode.getCategories()
		for cat in categories:
			c =  any(re.findall(catCheck, cat, re.IGNORECASE))
			if c:
				print('(C)', end='')
				return True

		return False

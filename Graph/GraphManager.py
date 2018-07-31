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
class GraphManager:



	def __init__(self):
		self.nodes = {}
		self.populatedNodes = {};

	def saveGraph(self, name):
		print("Saving graph...", end ='')
		GraphWriter.writeGraph(self.nodes, 'GraphData/'+ name + '_graphData.lgf')
		pickle.dump(self.nodes, open('GraphData/'+ name +'_graphNodes.p', "wb"))
		print("Save complete!")

	def readGraph(self, name):
		print("Reading in graph... ", end='')
		self.nodes = pickle.load(open("GraphData/" + name + "_graphNodes.p", "rb"))
		print("Loaded successfully")

	def dive(self):
		#tmp = self.nodes
		for item in list(self.nodes.keys()):
			for node in self.nodes[item].getConnections().values():
				#print('sending in :', node)
				self.populateTopicNode(node);

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

	def beginSearch(self, currentNode, currentDepth, depth):
		if currentDepth >= depth:
			return
		self.populateTopicNode(currentNode)
		currentLevelLinks = currentNode.getConnections().values();

		for item in list(currentLevelLinks):
			self.beginSearch(item, currentDepth+1, depth)

	def w_populateTopicNode(self, node):
		try:
			return self.populateTopicNode(node)
		except Exception as e:
			print("ERROR IN POPNODE:\n", e)
			return None

	def p_beginSearch(self, startingNode, depth):

		#pool = Pool(cpu_count() * 2)
		current_depth = 1
		#pool.map(self.populateTopicNode, [startingNode])
		self.populateTopicNode(startingNode)
		self.nodes[startingNode.getTopic().getName()] = startingNode
		if depth == 1:
			return

		currentNode = startingNode
		nodesPopulated = [currentNode]
		connections = []
		merger = []
		pool = Pool(cpu_count())
		for currentDepth in range(1, depth):
			print('=' * 70)
			print("=  At depth", currentDepth)
			connections = []
			for item in nodesPopulated:
				if item != None:
					if item.isPopulated():
						for otherItem in list(item.getConnections().values()):
							if otherItem != None:
								connections.append(otherItem)
			print("=  Current number of connections:",len(connections))
			print("=  Current number of NodesPopulated in this iteration: ",len(nodesPopulated))
			print("=  Total number of nodes",len(self.nodes.keys()))
			name = 'currentBatch'
			#pickle.dump(connections, open('GraphData/'+ name +'_graphNodes.p', "wb"))
			nodesPopulated = pool.map(self.w_populateTopicNode, connections)
			print('\n=  Successfully populated another round of nodes')
			for node in nodesPopulated:
				if node != None:
					if item.isPopulated():
						self.nodes[node.getTopic().getName()] = node
					#self.populatedNodes[node.getTopic().getName()] = True;
			print('=  Updated self.nodes\n')

		pool.close()
		pool.join()

		print('\nCount = ',len(list(self.nodes.keys())))
		return

	def populateTopicNode(self, node):
		print("1. Entered: ",end='')

		print(node.getTopic().getName())
		keyxyz = node.getTopic().getName()
		if(node.isPopulated()):
			return None
		print(keyxyz,'2. Checked isPopulated')
		#before performing operations-- we must validate the info of given TopicNode
		try:
			sourceCode = WebTool.getValidatedTopicSourceCode(node.getTopic().getName())
		except Exception as e:
			print("ERROR IN WEBTOOL:\n", e)
			return None

		print(keyxyz,'3. Got topic html source')
		sourceElement = SourceElement(sourceCode)
		print(keyxyz,'4. Created source element')
		sourceElement.validateName(node)
		print(keyxyz,'5. validated name')
		if(node.getTopic().getName() in self.nodes):
			return None
		try:
			links = sourceElement.grabIntroAndSeeAlsoLinks(node)
		except Exception as e:
			print("ERROR IN grabintro:\n", e)
			return None
		if links == None:
			return None
		print(keyxyz,'6. got links')
		print(node.getTopic(), '|', end='')
		self.addInfoToNewNodes(node, links)
		print()
		print(keyxyz,'7. added info to new links(nodes)')
		node.setCategory(sourceElement.getCategories())
		print(keyxyz,'8. set categories')
		node.setIsPopulated()
		print(keyxyz,'9. set node to populated')
		self.createConnectionDetails(node)
		print(keyxyz,'10. added connection details')
		print()
		if dill.pickles(node):
			return node
		else:
			print( dill.detect.badtypes(node, depth=1).keys())
			quit()
			return None
		#print(node)

	def addInfoToNewNodes(self, node, links):
		for link in list(links.keys()):
			nextTopic = Topic(link)
			nextTopicNode = TopicNode(nextTopic)
			#SourceElement.staticValidateName(nextTopicNode)
			try:
				SourceElement.staticValidation(nextTopicNode)
			except Exception as e:
				print("ERROR IN STATIC EVAL:\n", e)
				continue
			if(self.isBadLink(nextTopicNode)):
				continue
			#node.setDetailingName(nextTopic, links[link])
			node.setDetailingName(nextTopic, links[link])
			node.addConnection(nextTopic, nextTopicNode);
			print('✓', end='')


	def createConnectionDetails(self, node):
		for con in node.getConnections().keys():
			name = re.escape(node.getDetailingName(con))
			m = re.search(("\.(.*)" + name), node.getIntroText())
			if(m == None):
				m = re.search(("[\r\n]+(.*)" + name), node.getIntroText())
				if(m == None):
					continue
			#WILL PRODUCE weird errors if behind decimals or ellipse grammar
			mn = re.search(name+"(.*)\.", node.getIntroText())
			if(mn != None):
				text = m.group()[1:-(len(name))] + ' ' +mn.group()
				text = re.sub('\[\d+\]', '',text)
				node.addConnectionDetail(con, text)



	def isBadLink(self, topicNode):
		name = topicNode.getTopic().getName()
		n = any(re.findall('List of|Wikipedia|File:', name, re.IGNORECASE))
		if n:
			print('(N)',  end='')
			return True
		#check categories
		catCheck = 'outline of|portal:|list |lists |history of|glossary of|index of|wikipedia|file|help|template|category:'
		categories = topicNode.getCategories()
		for cat in categories:
			c =  any(re.findall(catCheck, cat, re.IGNORECASE))
			if c:
				print('(C)', end='')
				return True

		return False

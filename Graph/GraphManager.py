import sys, re,urllib,requests, codecs, operator, gzip, timeit, io
from bs4 import BeautifulSoup, NavigableString
from Graph.TopicNode import TopicNode
from Graph.Topic import Topic
from BSHelpers.WebTool import WebTool
from BSHelpers.SourceElement import SourceElement
from FileWriters.GraphWriter import GraphWriter
import pickle, dill
from functools import partial
from itertools import repeat
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

	def p_beginSearch(self, startingNode, depth):

		#pool = Pool(cpu_count() * 2)
		current_depth = 1
		#pool.map(self.populateTopicNode, [startingNode])
		self.populateTopicNode(startingNode)
		if depth == 1:
			return

		currentNode = startingNode
		nodesPopulated = [currentNode]
		connections = []
		merger = []
		pool = Pool(cpu_count() * 2)
		for currentDepth in range(1, depth):
			print('A')
			connections = []

			print(len(list(self.nodes.values())))
			print('B')
			for item in nodesPopulated:
				if item != None:
					if item.isPopulated():
						connections +=list(item.getConnections().values())
			print('C')
			print("con",len(connections))
			print("nodesPopulated",len(nodesPopulated))
			print("self.nodes",len(self.nodes.keys()))
			nodesPopulated = pool.map(self.populateTopicNode, connections)
			print('C.2')
			for node in nodesPopulated:
				if node != None:
					if item.isPopulated():
						print('C.3')
						self.nodes[node.getTopic().getName()] = node
					#self.populatedNodes[node.getTopic().getName()] = True;

		pool.close()
		pool.join()

		print('\nCount = ',len(list(self.nodes.keys())))
		return

	def populateTopicNode(self, node: TopicNode):
		print('D', end='')
		if(node.getTopic().getName() in self.nodes):
			return None
		print('E', end='')
		#before performing operations-- we must validate the info of given TopicNode
		sourceCode = WebTool.getValidatedTopicSourceCode(node.getTopic().getName())
		sourceElement = SourceElement(sourceCode)
		sourceElement.validateName(node)
		if(node.getTopic().getName() in self.nodes):
			return None
		print(node.getTopic(), '|', end='')
		#adds TopicNode to graph once validated
		self.nodes[node.getTopic().getName()] = node
		links = sourceElement.grabIntroAndSeeAlsoLinks(node)
		node.setCategory(sourceElement.getCategories())
		self.addInfoToNewNodes(node, links)
		node.setIsPopulated()
		print()
		#at end we check the current node off as 'populated'
		#self.populatedNodes[node.getTopic().getName()] = True;
		self.createConnectionDetails()
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
			SourceElement.staticValidation(nextTopicNode)
			if(self.isBadLink(nextTopicNode)):
				continue
			#node.setDetailingName(nextTopic, links[link])
			node.setDetailingName(nextTopic, link)
			node.addConnection(nextTopic, nextTopicNode);
			print('✓', end='')


	def createConnectionDetails(self):
		for node in self.nodes.values():
			if node.isPopulated() == False:
				continue
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
					#print("Relation between", node.getTopic().getName(), "and", name, "is", m.group() + mn.group()[len(name):])
					node.addConnectionDetail(con, m.group() + mn.group())


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

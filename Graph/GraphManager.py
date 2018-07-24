import sys, re,urllib,requests, codecs, operator, gzip, timeit, io
from bs4 import BeautifulSoup, NavigableString
from Graph.TopicNode import TopicNode
from Graph.Topic import Topic
from BSHelpers.WebTool import WebTool
from BSHelpers.SourceElement import SourceElement
from FileWriters.GraphWriter import GraphWriter
import pickle
from functools import partial
from itertools import repeat
from multiprocessing import Pool, cpu_count, Manager
from multiprocessing.managers import BaseManager
class GraphManager:



	nodes = {}
	populatedNodes = {};

	def init():
		manager = Manager()
		GraphManager.populatedNodes = manager.dict();
		#topic name maps to TopicNode
		GraphManager.nodes = manager.dict();

	def saveGraph():
		print("Saving graph...", end ='')
		GraphWriter.writeGraph(GraphManager.nodes, 'GraphData/graphData.lgf')
		pickle.dump(GraphManager.nodes, open("GraphData/graphNodes.p", "wb"))
		pickle.dump(GraphManager.populatedNodes, open("GraphData/populatedGraphNodes.p", "wb"))
		print("save complete!")

	def readGraph():
		print("Reading in graph... ", end='')
		GraphManager.nodes = pickle.load(open("GraphData/graphNodes.p", "rb"))
		GraphManager.populatedNodes = pickle.load(open("GraphData/populatedGraphNodes.p", "rb"))
		print("Loaded successfully")

	def dive():
		#tmp = GraphManager.nodes
		for item in list(GraphManager.nodes.keys()):
			for node in GraphManager.nodes[item].getConnections().values():
				#print('sending in :', node)
				GraphManager.populateTopicNode(node);

	def p_dive():
		#tmp = GraphManager.nodes
		pool = Pool(cpu_count() *2)
		for item in list(GraphManager.nodes.keys()):
			cons = list(GraphManager.nodes[item].getConnections().values())
			print('waiting')
			nodesPopulated = pool.map(GraphManager.populateTopicNode, cons)
			print('Home!')

			print('finished diving')
			for node in nodesPopulated:
				if(node != None):
					GraphManager.nodes[node.getTopic().getName()] = node
					GraphManager.populatedNodes[node.getTopic().getName()] = True;
		pool.close()
		pool.join()

	def beginSearch(currentNode, currentDepth, depth):
		if currentDepth >= depth:
			return
		GraphManager.populateTopicNode(currentNode)
		currentLevelLinks = currentNode.getConnections().values();

		for item in list(currentLevelLinks):
			GraphManager.beginSearch(item, currentDepth+1, depth)

	def p_beginSearch(startingNode, depth):

		pool = Pool(cpu_count() * 2)
		current_depth = 1
		#pool.map(GraphManager.populateTopicNode, [startingNode])
		GraphManager.populateTopicNode(startingNode)
		if depth == 1:
			return

		currentNode = startingNode
		nodesPopulated = [currentNode]
		connections = []
		merger = []
		for currentDepth in range(1, depth):
			connections = []
			print(len(list(GraphManager.nodes.values())))
			for item in nodesPopulated:
				if item == None:
					continue
				connections +=list(item.getConnections().values())

			nodesPopulated = pool.map(GraphManager.populateTopicNode, connections)
			merger = list(set(merger + nodesPopulated))
			for node in merger:
				if(node != None):
					GraphManager.nodes[node.getTopic().getName()] = node
					#GraphManager.populatedNodes[node.getTopic().getName()] = True;

		pool.close()
		pool.join()

		print('\nCount = ',len(list(GraphManager.nodes.keys())))
		return

	def populateTopicNode(node: TopicNode):
		if(node.getTopic().getName() in GraphManager.nodes):
			return None


		#before performing operations-- we must validate the info of given TopicNode
		sourceCode = WebTool.getValidatedTopicSourceCode(node.getTopic().getName())
		sourceElement = SourceElement(sourceCode)
		sourceElement.validateName(node)
		if(node.getTopic().getName() in GraphManager.nodes):
			return None
		print(node.getTopic(), '|', end='')
		#adds TopicNode to graph once validated
		GraphManager.nodes[node.getTopic().getName()] = node

		links = sourceElement.grabIntroAndSeeAlsoLinks(node)
		node.setCategory(sourceElement.getCategories())
		GraphManager.addInfoToNewNodes(node, links)
		node.setIsPopulated()

		print()
		#at end we check the current node off as 'populated'
		#GraphManager.populatedNodes[node.getTopic().getName()] = True;
		GraphManager.createConnectionDetails()
		return node
		#print(node)

	def addInfoToNewNodes(node, links):
		for link in list(links.keys()):
			nextTopic = Topic(link)
			nextTopicNode = TopicNode(nextTopic)
			#SourceElement.staticValidateName(nextTopicNode)
			SourceElement.staticValidation(nextTopicNode)
			if(GraphManager.isBadLink(nextTopicNode)):
				print('X', end='')
				return
			#node.setDetailingName(nextTopic, links[link])
			node.setDetailingName(nextTopic, link)
			node.addConnection(nextTopic, nextTopicNode);
			print('✓', end='')


	def createConnectionDetails():
		for node in GraphManager.nodes.values():
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


	def isBadLink(topicNode):
		name = topicNode.getTopic().getName()
		if any(re.findall('Wikipedia', name, re.IGNORECASE)):
			print('(N)',  end='')
			return True

		#check categories
		catCheck = 'outline of|portal:|list |lists |history of|glossary of|index of|wikipedia|file|help|template|category:'
		categories = topicNode.getCategories()
		for cat in categories:
			if any(re.findall(catCheck, cat, re.IGNORECASE)):
				print('(C)', end='')
				#print('!',cat,'!', end='')
				return True

		return False

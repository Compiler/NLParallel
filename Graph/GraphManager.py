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

	def saveGraphPooled(nodesToWrite):
		print("Saving graph...", end ='')
		GraphWriter.writeGraph(nodesToWrite, 'GraphData/graphData.lgf')
		pickle.dump(nodesToWrite, open("GraphData/graphNodes.p", "wb"))
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

	def beginSearch(currentNode, currentDepth, depth):
		if currentDepth > depth:
			return
		GraphManager.populateTopicNode(currentNode)
		currentLevelLinks = currentNode.getConnections().values();

		for item in list(currentLevelLinks):
			GraphManager.beginSearch(item, currentDepth+1, depth)

	def beginSearchPooled(startingNode, depth):

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
				currentNode = item
				connections +=list(currentNode.getConnections().values())

			print('!')
			nodesPopulated = pool.map(GraphManager.populateTopicNode, connections)
			merger = list(set(merger + nodesPopulated))



		print('\nCount = ',len(merger) + 1)
		return

	def populateTopicNode(node: TopicNode):
		if(node.getTopic().getName() in GraphManager.populatedNodes):
			return


		#before performing operations-- we must validate the info of given TopicNode
		sourceCode = WebTool.getValidatedTopicSourceCode(node.getTopic().getName())
		sourceElement = SourceElement(sourceCode)
		sourceElement.validateName(node)
		if(node.getTopic().getName() in GraphManager.populatedNodes):
			return
		print(node.getTopic(), '|', end='')
		#sys.stdout.flush()
		#adds TopicNode to graph once validated
		GraphManager.nodes[node.getTopic().getName()] = node
		links = sourceElement.grabIntroAndSeeAlsoLinks(node)


		for link in list(links.keys()):
			nextTopic = Topic(link)
			if(GraphManager.isBadLink(nextTopic)):
				print('X', end='')
				continue
			nextTopicNode = TopicNode(nextTopic)
			SourceElement.staticValidateName(nextTopicNode)
			if(GraphManager.isBadLink(nextTopic)):
				print('X', end='')
				continue
			node.setDetailingName(nextTopic, links[link])
			node.addConnection(nextTopic, nextTopicNode);
			print('✓', end='')
		sys.stdout.flush()
		print()
		#at end we check the current node off as 'populated'
		GraphManager.populatedNodes[node.getTopic().getName()] = True;
		GraphManager.createConnectionDetails()
		return node
		#print(node)


	def createConnectionDetails():
		for item in GraphManager.populatedNodes.keys():
			node = GraphManager.nodes[item]

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

	def isBadLink(topic):
		name = topic.getName()
		if(re.search('(Wikipedia)', name) == None):
			return False

		return True

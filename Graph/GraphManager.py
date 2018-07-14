import sys, re,urllib,requests, codecs, operator, gzip, timeit, io
from bs4 import BeautifulSoup, NavigableString
from Graph.TopicNode import TopicNode
from Graph.Topic import Topic
from BSHelpers.WebTool import WebTool
from BSHelpers.SourceElement import SourceElement
from FileWriters.GraphWriter import GraphWriter
import pickle


class GraphManager:
	populatedNodes = {};
	#topic name maps to TopicNode
	nodes = {};

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

	def beginSearch(currentNode, currentDepth, depth):
		if currentDepth > depth:
			return
		GraphManager.populateTopicNode(currentNode)
		currentLevelLinks = currentNode.getConnections().values();

		for item in list(currentLevelLinks):
			GraphManager.beginSearch(item, currentDepth+1, depth)


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
		#adds TopicNode to graph once validated
		GraphManager.nodes[node.getTopic().getName()] = node
		links = sourceElement.grabIntroAndSeeAlsoLinks()

		for link in links:
			nextTopic = Topic(link)
			nextTopicNode = TopicNode(nextTopic)
			SourceElement.staticValidateName(nextTopicNode)
			node.addConnection(nextTopic, nextTopicNode);
			print('->', end='')
		print()
		#at end we check the current node off as 'populated'
		GraphManager.populatedNodes[node.getTopic().getName()] = True;
		#print(node)

import sys, re,urllib,requests, codecs, operator, gzip, timeit, io
from bs4 import BeautifulSoup, NavigableString
from Graph.TopicNode import TopicNode
from Graph.Topic import Topic
from BSHelpers.WebTool import WebTool
from BSHelpers.SourceElement import SourceElement
from FileWriters.GraphWriter import GraphWriter


class GraphManager:
	populatedNodes = {};
	nodes = {};

	def beginSearch(node: TopicNode, depth: int):
		GraphManager.populateTopicNode(node)
		for i in range(depth-1):
			for item in list(node.getConnections().values()):
				GraphManager.populateTopicNode(item)

		GraphWriter.writeGraph(GraphManager.nodes, 'graphData.lpf')

	def populateTopicNode(node: TopicNode):
		if(node.getTopic().getName() in GraphManager.populatedNodes):
			return


		#before performing operations-- we must validate the info of given TopicNode
		sourceCode = WebTool.getValidatedTopicSourceCode(node.getTopic().getName())
		sourceElement = SourceElement(sourceCode)
		sourceElement.validateName(node)
		if(node.getTopic().getName() in GraphManager.populatedNodes):
			return
		print("Populating", node.getTopic())
		#adds TopicNode to graph once validated
		GraphManager.nodes[node.getTopic().getName()] = node
		links = sourceElement.grabIntroAndSeeAlsoLinks()

		for link in links:
			nextTopic = Topic(link)
			node.addConnection(nextTopic, TopicNode(nextTopic));

		#at end we check the current node off as 'populated'
		GraphManager.populatedNodes[node.getTopic().getName()] = True;
		#print(node)
		print('\n')

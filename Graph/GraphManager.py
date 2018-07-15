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
		#sys.stdout.flush()
		#adds TopicNode to graph once validated
		GraphManager.nodes[node.getTopic().getName()] = node
		links = sourceElement.grabIntroAndSeeAlsoLinks(node)


		for link in links:
			nextTopic = Topic(link)
			if(GraphManager.isBadLink(nextTopic)):
				print('X', end='')
				continue
			nextTopicNode = TopicNode(nextTopic)
			SourceElement.staticValidateName(nextTopicNode)
			if(GraphManager.isBadLink(nextTopic)):
				print('X', end='')
				continue
			node.addConnection(nextTopic, nextTopicNode);
			print('✓', end='')
		sys.stdout.flush()
		print()
		#at end we check the current node off as 'populated'
		GraphManager.populatedNodes[node.getTopic().getName()] = True;
		GraphManager.createConnectionDetails()
		#print(node)


	def createConnectionDetails():
		for item in GraphManager.populatedNodes.keys():
			node = GraphManager.nodes[item]
			for con in node.getConnections().keys():
				name = con.getName()
				m = re.match(("\.(.*)" + name), node.getIntroText())
				if(m == None):
					m = re.match(("[\r\n]+(.*)" + name), node.getIntroText())
					if(m == None):
						continue

					#WILL PRODUCE weird errors if behind decimals or ellipse grammar
					mn = re.match((name+"(.*)\."), node.getIntroText())
					if(mn != None):
						print("Relation between", node.getTopic().getName(), "and", name, "is", m.group(1) + mn.group(1))
						node.addConnectionDetail(con, m.group(1) + mn.group(1))

				print(m.group(0))

	def isBadLink(topic):
		name = topic.getName()
		if(re.search('(Wikipedia)', name) == None):
			return False

		return True

import sys, re,urllib,requests, codecs, operator, gzip, timeit, io
from bs4 import BeautifulSoup, NavigableString
from Graph.TopicNode import TopicNode
from Graph.Topic import Topic
from BSHelpers.WebTool import WebTool
from BSHelpers.SourceElement import SourceElement



class GraphManager:

	nodes = {};
	def populateTopicNode(node: TopicNode):
		print("Populating", node.getTopic())
		GraphManager.nodes[node.getTopic().getName()] = node
		GraphManager.getTopicConnectionList(node.getTopic().getName());




	#First part invokes method that pings network
	def getTopicConnectionList(title):
		try: sourcecode = WebTool.getTopicSourceCode(title)
		except:
			try: sourcecode = WebTool.getTopicSourceCode(urllib.quote(title))
			except:
				print('FAILED: Could not load', title)
				return {}

		try:soupobj = BeautifulSoup(sourcecode, WebTool.parser)
		except: print('FAILED: to get soupobj')

		main_name = soupobj.find("h1")
		main_name = main_name.text

		redirect = soupobj.find('span', {'class':'mw-redirectedfrom'})


		if redirect != None:
			redirect_from_name = (redirect.find('a', {'class':'mw-redirect'})).text
			print(url, ' redirected from ', redirect_from_name)

		print("Finished")

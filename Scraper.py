import sys
import re
from bs4 import BeautifulSoup, NavigableString
import urllib
import requests
import codecs
import operator
import gzip
import timeit
import io

from TopicNode import TopicNode
from Topic import Topic



class Scraper:
	parser = 'lxml'

	def populateTopicNode(node: TopicNode):
		print("Populating ", node.getTopic())

	#Gets the html of the page given end half of url (just the topic)
	def getTopicSourceCode(topic: str):
	    opener = urllib.request.build_opener()
	    opener.addheaders = [('User-agent', 'MyTestScript/1.0 (contact at myscript@mysite.com)'), ('Accept-encoding', 'gzip')]
	    resource = opener.open("http://en.wikipedia.org/wiki/" + topic)
	    if resource.info().get('Content-Encoding') == 'gzip':
	        return gzip.GzipFile(fileobj=io.BytesIO( resource.read())).read()
	    else:
	        return resource.read()




	def getLinks(title):
		try: sourcecode = getTopicSourceCode(url)
		except:
			try: sourcecode = getTopicSourceCode(urllib.quote(url))
			except:
				print('!Could not load',url)
				return {}

		try:
			soupobj = BeautifulSoup(sourcecode, parser)
		except:
			print('failed to get soupobj')
			return {}

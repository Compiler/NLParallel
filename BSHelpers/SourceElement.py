import sys, re,urllib,requests, codecs, operator, gzip, timeit, io
from bs4 import BeautifulSoup, NavigableString
from Graph.TopicNode import TopicNode
from Graph.Topic import Topic



#Class will do operations that do NOT require pinging network or dealing with
#driver... will need BeautifulSoup object
class SourceElement:

	def __init__(self, source):
		self.source = source
		#do some stuff with source

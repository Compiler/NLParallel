import sys, re,urllib,requests, codecs, operator, gzip, timeit, io
from bs4 import BeautifulSoup, NavigableString
from Graph.TopicNode import TopicNode
from Graph.Topic import Topic
from BSHelpers.WebTool import WebTool



#Class will do operations that do NOT require pinging network or dealing with
#driver... will need BeautifulSoup object
class SourceElement:

	def __init__(self, source):
		self.source = source
		try:self.soup = BeautifulSoup(self.source, WebTool.parser)
		except: print('FAILED: to get self.soup')
		#do some stuff with source

	def validateName(self, topic):
		#redirect = self.soup.find('span', {'class':'mw-redirectedfrom'})
		#if(redirect != None):
		mainName = self.soup.find("h1")
		mainName = mainName.text
		topic.setTopicName(mainName)

	def staticValidateName(topic):
		if(topic.nameValidated):
			 return
			 
		source = WebTool.getValidatedTopicSourceCode(topic.getTopic().getName());
		try:soup = BeautifulSoup(source, WebTool.parser)
		except: print('FAILED: to get self.soup')
		mainName = soup.find("h1")
		mainName = mainName.text
		topic.setTopicName(mainName)



	def grabIntroAndSeeAlsoLinks(self):
		links = {}
		self.grabIntroLinks(links)
		self.grabSeeAlsoLinks(links)

		return list(links.keys())
	def grabIntroLinks(self, links):
		intro = self.soup.find("div", {'class':'mw-parser-output'}).findAll();
		for element in intro:
			if element.name == 'h2':
				break;
			if element.name == 'p':
				introLinks = element.findAll('a', attrs={'href' : re.compile('^/wiki/')})
				for element in introLinks:
					links[element['href'][6:]] = 1

		return links

	def grabSeeAlsoLinks(self, links):
		contents_section = self.soup.find("div", {'id' : 'toc'})
		if contents_section != None:
			for element in contents_section.contents:
				if element.name == 'ul':
					contents_list = element.findAll('a', attrs={'href' : re.compile('^#')})
					for items in contents_list:
						if items.get('href') == '#See_also':
							see_also_section = self.soup.findAll(attrs={"id":'See_also'})#, {'class':'mw-headline'})
							parent = see_also_section[0].parent
							link_section = parent.findNext('ul', attrs={'style':None})
							seeAlsoLinks = link_section.findAll('a', attrs={'href' : re.compile('^/wiki/')})
							for element in seeAlsoLinks:
								links[element['href'][6:]] = 1

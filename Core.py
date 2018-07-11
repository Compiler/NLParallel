from TopicNode import TopicNode
from Topic import Topic
from Scraper import Scraper





if __name__ == '__main__':
	print('hello')
	topicNode = TopicNode(Topic('Mathematics'))
	Scraper.populateTopicNode(topicNode)
	Scraper.getTopicSourceCode('mathematics')

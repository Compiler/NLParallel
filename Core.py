from Graph.TopicNode import TopicNode
from Graph.Topic import Topic
from Graph.GraphManager import GraphManager





if __name__ == '__main__':
	topicNode = TopicNode(Topic('Mathematics'))
	GraphManager.populateTopicNode(topicNode)

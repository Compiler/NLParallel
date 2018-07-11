import Topic

class TopicNode:

	#connections is a map of Topic->TopicNode
	def __init__(self, topic):
		self.topic = topic;
		self.connections = {};

	#uses a Topic to TopicNode relationship
	def addConnection(self, topic, topicNode):
		self.connections[topic] = topicNode;

	def getTopic(self):
		return self.topic

	def __str__(self):
		if len(self.connections) == 0:
			return '{} {}'.format(self.topic.getName() , "connects to nothing.")
		else:
			return '{} {} {}'.format(self.topic.getName() , "connects to", list(self.connections.keys()))

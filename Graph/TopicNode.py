from Graph.Topic import Topic

class TopicNode:

	#connections is a map of Topic->TopicNode
	def __init__(self, topic):
		self.topic = topic;
		self.connections = {};
		self.sourceCode = None;
		self.mainName = None;

	#uses a Topic to TopicNode relationship
	def addConnection(self, topic, topicNode):
		self.connections[topic] = topicNode;

	def getConnections(self):
		return self.connections
	def getTopic(self):
		return self.topic

	def setTopicName(self, newName):
		self.topic.setName(newName);

	def __str__(self):
		if len(self.connections) == 0:
			return '{} {}'.format(self.topic.getName() , "connects to nothing.")
		else:
			val = ''
			for item in self.connections.keys():
				val = val + item.getName() + ", "
			return '{} {} {}'.format(self.topic.getName() , "connects to", val)

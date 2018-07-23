from Graph.Topic import Topic

class TopicNode:

	#connections is a map of Topic->TopicNode
	def __init__(self, topic):
		self.topic = topic;
		self.connections = {};
		self.connectionDetails={};
		self.introText = None;
		self.detailingName = {};#ConnectingTopic->str(name)
		self.mainName = None;
		self.nameValidated = False
		self.categories = []


	def setDetailingName(self,topic, text):
		self.detailingName[topic] = text
	def getDetailingName(self, topic):
		return self.detailingName[topic]

	def addCategory(self, cat):
		self.categories.append(cat)

	def setCategory(self, cats):
		self.categories = cats

	def getCategory(self):
		return self.categories

	def setIntroText(self, text):
		self.introText = text
	def getIntroText(self):
		return self.introText
	#uses a Topic to TopicNode relationship
	def addConnection(self, topic, topicNode):
		self.connections[topic] = topicNode;

	def addConnectionDetail(self, topic, details):
		self.connectionDetails[topic] = details;

	def getConnections(self):
		return self.connections

	def getTopic(self):
		return self.topic

	def setNameValidated(self, flag):
		self.nameValidated = flag
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

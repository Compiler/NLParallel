from Graph.Topic import Topic

class TopicNode:

	#connections is a map of Topic->TopicNode
	def __init__(self, topic):
		self.topic = topic;
		self.connections = {};
		self.connectionDetails={}; #Topic->details(str)
		self.introText = None;
		self.detailingName = {};#ConnectingTopic->str(name)
		self.mainName = None;
		self.nameValidated = False
		self.categories = []
		self.populated = False
		self.depthFound = 0


	def setDepthFound(self, depth):
		self.depthFound = depth

	def getDepthFound(self):
		return self.depthFound

	def isPopulated(self):
		return self.populated

	def setIsPopulated(self):
		self.populated = True

	def setDetailingName(self,topic, text):
		self.detailingName[topic] = text
	def getDetailingName(self, topic):
		return self.detailingName[topic]

	def addCategory(self, cat):
		self.categories.append(cat)

	def setCategory(self, cats):
		self.categories = cats


	def getCategories(self):
		return self.categories

	def setIntroText(self, text):
		self.introText = text
	def getIntroText(self):
		return self.introText
	#uses a Topic to TopicNode relationship
	def addConnection(self, topic, topicNode):
		self.connections[topic] = topicNode;
	#uses a Topic to TopicNode relationship
	def addConnection(self, topicNode):
		self.connections[topicNode.getTopic()] = topicNode;

	def addConnectionDetail(self, topic, details):
		self.connectionDetails[topic] = details;
	def getConnectionDetail(self, topic):
		if topic in self.connectionDetails:
			return self.connectionDetails[topic]
		else:
			print(topic, 'is not in', self.topic,'set of connections... options:\n')
			#for i in self.connectionDetails.keys():
				#print(i.getName(), ', ',end ='')
	def getConnections(self):
		return self.connections

	def getTopic(self):
		return self.topic

	def setNameValidated(self, flag):
		self.nameValidated = flag
	def setTopicName(self, newName):
		self.topic.setName(newName);

	def detailingText(self):
		val = self.topic.getName() +' is connected to ' + (str)(len(self.connections.keys())) + ' different topics:\n'
		for i in list(self.connections.keys()):
			val = val + i.getName() + ', ';
		val += '\n' + self.topic.getName() + ' is in the category of: \n'
		for i in self.categories:
			val += i + ', '
		return val


	def __str__(self):
		if len(self.connections) == 0:
			return '{} {}'.format(self.topic.getName() , "connects to nothing.")
		else:
			val = ''
			for item in self.connections.keys():
				val = val + item.getName() + ", "
			return '{} {} {}'.format(self.topic.getName() , "connects to", val)

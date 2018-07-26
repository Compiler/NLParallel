
class SearchUtils:



	def __init__(self, nodes):
		self.nodes = nodes
	#graphNodes, string a, string b
	#returns topicNodes in order

	def updateGraph(self, nodes):
		self.nodes = nodes

	def __findAllPaths(self, a, b, visited, path):
		visited[a]= True
		path.append(a)
		if a == b:
			if(len(path) < 5):
				print(path)
		else:
			if a not in self.nodes:
				return
			cur = self.nodes[a]
			for i in cur.getConnections().values():
				if i.getTopic().getName() not in visited:
					self.__findAllPaths(i.getTopic().getName(), b, visited, path)
				elif visited[i.getTopic().getName()] == False:
					self.__findAllPaths(i.getTopic().getName(), b, visited, path)
		path.pop()
		visited[a]= False


	def findAllPaths(self, a, b):
		visited = {}
		path = []
		self.__findAllPaths(a, b, visited, path)

import sys
from queue import PriorityQueue

class SearchUtils:



	def __init__(self, nodes):
		self.nodes = nodes
	#graphNodes, string a, string b
	#returns topicNodes in order

	def updateGraph(self, nodes):
		self.nodes = nodes


	def dijkstra(self, source, goal):
		visited = {}
		parent = {source: None}
		distance = {source: 0}
		queue = PriorityQueue()


		edgeWeight = 1

		for key in self.nodes.keys():
			distance[key] = sys.maxsize
			for oth in self.nodes[key].getConnections().keys():
				distance[oth.getName()] = sys.maxsize

		distance[source] = 0


		queue.put((distance[source], source))
		while queue.empty() == False:
			currentShortest = queue.get()[1]
			if currentShortest not in self.nodes:
				if(currentShortest == goal):
					curDistance = distance[currentShortest] + edgeWeight
					if curDistance < distance[currentShortest]:
						distance[currentShortest] = curDistance
						parent[currentShortest] = currentShortest
				visited[currentShortest] = None
				continue
			for node in self.nodes[currentShortest].getConnections().keys():
				node = node.getName()
				if node in visited:
					continue
				curDistance = distance[currentShortest] + edgeWeight
				if curDistance < distance[node]:
					distance[node] = curDistance
					parent[node] = currentShortest
					queue.put((distance[node], node))
				visited[currentShortest] = None
		if goal not in distance:
			print('no path found')
			return
		node = goal
		print(distance[goal])
		path = []
		while parent[node] != None:
			path.append(node)
			node = parent[node]
		path.append(source)
		return path

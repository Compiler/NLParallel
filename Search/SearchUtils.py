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




		queue.put((distance[source], source))
		while queue.empty() == False:
			currentShortest = queue.get()
			for node in self.nodes[currentShortest].getConnections().keys():
				if node in visited:
					continue
				curDistance = distance[currentShortest] + edgeWeight
				if curDistance < distance[node]:
					distance[node] = curDistance
				parent[node] = currentShortest
				queue.put((distance[node], node))
				visited[currentShortest]



class GraphWriter:


	def writeGraph(graph, fileName):
		with open(fileName, 'w') as writer:
			for item in graph.keys():
				writer.write(item)
				for element in graph[item].getConnections().values():
					writer.write("\n->")
					writer.write(element.getTopic().getName())

				writer.write("\n=============")



class GraphWriter:


	def writeGraph(graph, fileName):
		tnCount = 1
		subtnCount = 1;
		with open(fileName, 'w') as writer:
			val = str(len(graph.keys()))
			writer.write(val)
			writer.write('\n')
			for item in graph.keys():
				try:
					writer.write('')
					writer.write(item)
					subtnCount = 1;
					tnCount += 1

					for element in graph[item].getConnections().values():
						writer.write("\n\t->")
						writer.write(element.getTopic().getName())

					writer.write("\n==========================================================\n")
				except:
					print("! ", END = '')

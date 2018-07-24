

class GraphWriter:


	def writeGraph(graph, fileName):
		tnCount = 1
		subtnCount = 1;
		with open(fileName, 'w') as writer:
			val = str(len(graph.keys()))
			writer.write(val)
			writer.write('\n')
			sortedKeys=sorted(graph.keys(), key=lambda x:x.lower())
			for item in sortedKeys:
				try:
					writer.write('')
					writer.write(item)
					subtnCount = 1;
					tnCount += 1
					todo = []
					for kk in list(graph[item].getConnections().keys()):
						todo.append(kk.getName())
					sortedValues=sorted(todo, key=str.lower)
					for element in sortedValues:
						writer.write("\n\t->")
						writer.write(element)

					writer.write("\n==========================================================\n")
				except:
					print("(!)", end = '')

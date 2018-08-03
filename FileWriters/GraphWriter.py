

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
					ot = str(graph[item].getDepthFound()) + '. '
					writer.write(ot)
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


	def writeSIFGraph(nodes, fileName):
		edge = 'edge'
		with open('NetworkSIFData/'+fileName+'.sif', 'w') as writer:
			for key in nodes.keys():
				for node in nodes[key].getConnections().keys():
					writer.write(key +'\t'+edge+'\t'+node.getName()+'\n')

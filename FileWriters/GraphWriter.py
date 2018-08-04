

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
					try:
						writer.write(key +'\t'+edge+'\t'+node.getName()+'\n')
					except:
						pass

	def writeGMLGraph(nodes, fileName):
		with open('NetworkData/GMLData/'+fileName+'.gml', 'w') as writer:
			writer.write('graph\n[')
			try:
				for key in nodes.keys():
					val = '  node [\n  name ' + key +'\n  label "' + key + '"\n  ]\n'
					for node in nodes[key].getConnections().keys():
						val += '  node [\n  name ' + node.getName() +'\n  label "' + node.getName() + '"\n  ]\n'
						writer.write(val)

				for key in nodes.keys():
					val = '  edge [\n  source ' + key +'\n  label "' + key + '"\n'
					for node in nodes[key].getConnections().keys():
						val += '  target ' + node.getName() +'\n]\n'
						writer.write(val)

			except:
				pass

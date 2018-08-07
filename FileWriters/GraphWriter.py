import re

class GraphWriter:


	def lgfToPickle(fileName):
		filePath = 'GraphData/'+fileName +'.lgf'
		with open(fileName, 'rb') as reader:
			pass




	def writeGraph(graph, fileName):
		tnCount = 1
		subtnCount = 1;
		with open(fileName, 'w') as writer:
			try:
				val = str(len(graph.keys()))
				writer.write(val)
				writer.write('\n')
				sortedKeys=sorted(graph.keys(), key=lambda x:x.lower())
				for item in sortedKeys:
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
			writer.write('graph\n[\n')
			try:
				for key in nodes.keys():
					print('re',len(list(nodes.keys())), ' - ', end = '')
					print(len(list(nodes[key].getConnections().keys())))
					myKey = key
					myKey = re.sub('[^\w]', '', myKey)
					myKey = re.sub('\s', '_', myKey)
					val = '  node [\n    id ' + myKey +'\n    label "' + key + '"\n  ]\n'
					print('re',len(list(nodes.keys())), ' - ', end = '')
					print(len(list(nodes[key].getConnections().keys())))
					for node in nodes[key].getConnections().keys():
						name = re.sub('[^\w]', '', node.getName())
						name = re.sub('\s', '_', name)
						#name = re.sub(',|\'|\.', '', name)
						val += '  node [\n    id ' + name +'\n    label "' + node.getName() + '"\n  ]\n'
						writer.write(val)
			except:
				print('fuck1')
			try:
				for key in nodes.keys():
					print(len(list(nodes.keys())), ' - ', end = '')
					print(len(list(nodes[key].getConnections().keys())))
					myKey = key
					myKey = re.sub('[^\w]', '', myKey)
					myKey = re.sub('\s', '_', myKey)

					print(len(list(nodes.keys())), ' - ', end = '')
					print(len(list(nodes[key].getConnections().keys())))
					if len(list(nodes[key].getConnections().keys())) != 0:
						for node in nodes[key].getConnections().keys():
							name = re.sub('[^\w]', '', node.getName())
							name = re.sub('\s', '_', name)
							val ='  edge [\n  source ' + myKey +'  ' + '\n' + '  target ' + name +'\n  ]\n'
							writer.write(val)
			except:
				print('fuck2')

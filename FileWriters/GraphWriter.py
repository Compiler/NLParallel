import re

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
			writer.write('graph\n[\n')
			#try:
			for key in nodes.keys():
				myKey = re.sub('[^\w]', '', key)
				myKey = re.sub('\s', '_', key)
				val = '  node [\n    id ' + myKey +'\n    label "' + key + '"\n  ]\n'
				for node in nodes[key].getConnections().keys():
					name = node.getName()
					name = re.sub('[^\w]', '', name)
					name = re.sub('\s', '_', name)
					#name = re.sub(',|\'|\.', '', name)
					val += '  node [\n    id ' + name +'\n    label "' + node.getName() + '"\n  ]\n'
					writer.write(val)
			#except:
				#print('fuck1')
			#try:
			for key in nodes.keys():
				myKey = re.sub('[^\w]', '', myKey)
				myKey = re.sub('\s', '_', myKey)
				for node in nodes[key].getConnections().keys():
					name = node.getName()
					name = re.sub('[^\w]', '', name)
					name = re.sub('\s', '_', name)
					print('.',end='')
					val = '  edge [\n  source ' + myKey +'  ' + '\n' + '  target ' + name +'\n  ]\n'
					writer.write(val)
			#except:
				#print('fuck2')

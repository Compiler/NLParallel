from Graph.TopicNode import TopicNode
from Graph.Topic import Topic
from Graph.GraphManager import GraphManager
from BSHelpers.SourceElement import SourceElement
import timeit, sys, codecs, pickle

from Search.SearchUtils import SearchUtils




if __name__ == '__main__':
	#depth = input('Enter the depth you want the tree to expand to: ')
	startTime = timeit.default_timer()
	#print('Beginning expansion...')

	graphManager = GraphManager()
	graphManager.p_beginSearch(TopicNode(Topic('Mathematics')), (int)(2))
	graphManager.saveGraph('p2');





	nodes = pickle.load(open("GraphData/p2_graphNodes.p", "rb"))
	print('Loaded')
	search = SearchUtils(nodes)
	if 'Mathematics' in nodes:
		print(True)
	if 'Bible' in nodes:
		print(True)
	path = search.dijkstra('Mathematics', 'World War II')
	sz = len(path)
	for i in range(0, sz-1):
		print(nodes[path[sz - i - 1]].getConnectionDetail(Topic(path[sz-i-2])))

	elapsedTime = timeit.default_timer() - startTime
	val = "{0:.2f}".format((elapsedTime / 60.0))
	print('Searched in', val, 'minutes.')

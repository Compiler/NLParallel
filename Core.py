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

	#graphManager = GraphManager()
	#graphManager.p_beginSearch(TopicNode(Topic('Mathematics')), (int)(4))
	#graphManager.saveGraph('p4');


	nodes = pickle.load(open("GraphData/p3_graphNodes.p", "rb"))
	print('Loaded')
	search = SearchUtils(nodes)
	if 'Mathematics' in nodes:
		print(True)
	if 'Bible' in nodes:
		print(True)
	path = search.dijkstra('Mathematics', 'Bible')
	sz = len(path)
	for i in range(0, sz):
		print(path[sz - i - 1], ' -> ', end = '')

	elapsedTime = timeit.default_timer() - startTime
	val = "{0:.2f}".format((elapsedTime / 60.0))
	#print('Created a',depth, 'deep search in ',val , 'minutes.')
	print('Searched in', val, 'minutes.')

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
	#graphManager.p_beginSearch(TopicNode(Topic('Mathematics')), (int)(depth))
	#graphManager.saveGraph('tester');

	nodes = pickle.load(open("GraphData/p3_graphNodes.p", "rb"))
	print('Loaded')
	search = SearchUtils(nodes)
	if 'Mathematics' in nodes:
		print(True)
	if 'Concept' in nodes:
		print(True)
	search.findAllPaths('Mathematics', 'Concept')

	elapsedTime = timeit.default_timer() - startTime
	val = "{0:.2f}".format((elapsedTime / 60.0))
	#print('Created a',depth, 'deep search in ',val , 'minutes.')
	print('Searched in', val, 'minutes.')

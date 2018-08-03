from Graph.TopicNode import TopicNode
from Graph.Topic import Topic
from Graph.GraphManager import GraphManager
from BSHelpers.SourceElement import SourceElement
import timeit, sys, codecs, pickle, os, psutil
from Search.SearchUtils import SearchUtils




if __name__ == '__main__':
	#depth = input('Enter the depth you want the tree to expand to: ')
	startTime = timeit.default_timer()
	#print('Beginning expansion...')
	#nltk.download('punkt')

	graphManager = GraphManager()
	graphManager.p_beginSearch(TopicNode(Topic('Mathematics')), (int)(6), True)
	#@graphManager.saveGraph('p1');
	elapsedTime = timeit.default_timer() - startTime
	val = "{0:.2f}".format((elapsedTime / 60.0))
	print('Populated graph in', val, 'minutes.')

	quit()

	nodes = pickle.load(open("GraphData/p2_graphNodes.p", "rb"))
	print('Loaded')
	search = SearchUtils(nodes)
	path = search.dijkstra('Mathematics', 'Truth')
	sz = len(path)
	for i in range(0, sz):
		print(path[sz - i - 1],  '->', end = '')
	print()
	for i in range(0, sz-1):
		print(nodes[path[sz - i - 1]].getConnectionDetail(Topic(path[sz-i-2])))
	process = psutil.Process(os.getpid())
	print((process.memory_info().rss)/ (1000 * 1000), 'mb of memory used.')
	elapsedTime = timeit.default_timer() - startTime
	val = "{0:.2f}".format((elapsedTime / 60.0))
	print('Searched in', val, 'minutes.')

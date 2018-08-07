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

	#graphManager = GraphManager()
	#graphManager.p_beginSearch(TopicNode(Topic('Mathematics')), (int)(5))
	#graphManager.saveGraph('p5');
	#elapsedTime = timeit.default_timer() - startTime
	#val = "{0:.2f}".format((elapsedTime / 60.0))
	#print('Populated graph in', val, 'minutes.')

	#quit()

	#nodes = pickle.load(open("GraphData/p2_graphNodes.p", "rb"))
	nodes = {}
	a = TopicNode(Topic('A'))
	c = TopicNode(Topic('C'))
	aa = TopicNode(Topic('AA'))
	aaa = TopicNode(Topic('AAA'))
	ab = TopicNode(Topic('AB'))
	ac = TopicNode(Topic('AC'))
	aca = TopicNode(Topic('ACA'))
	acc = TopicNode(Topic('ACC'))
	aba = TopicNode(Topic('ABA'))
	abb = TopicNode(Topic('ABB'))
	abc = TopicNode(Topic('ABC'))

	a.addConnection(aa);
	a.addConnection(ab);
	a.addConnection(ac);
	ab.addConnection(aba);
	ab.addConnection(abb);
	ab.addConnection(abc);
	aa.addConnection(aaa);
	aa.addConnection(ab);
	aa.addConnection(a);
	ac.addConnection(aca);
	ac.addConnection(a);
	ac.addConnection(acc);
	aaa.addConnection(aca);
	aaa.addConnection(ab)
	abc.addConnection(c)
	nodes['A'] = a; nodes['AA'] = aa; nodes['AB'] = ab; nodes['AC'] = ac;
	nodes['AAA'] = aaa; nodes['ABA'] = aba; nodes['ABB'] = abb; nodes['ABC'] = abc;
	nodes['ACA'] = aca; nodes['ACC'] = acc; nodes['C'] = c;

	#graphManager = GraphManager()
	#graphManager.saveGraph('test_graph');
	print('Loaded')
	#quit()
	search = SearchUtils(nodes)
	path = search.dijkstra('A', 'ACA')
	sz = len(path)
	for i in range(0, sz):
		print(path[sz - i - 1],  '->', end = '')
	quit()
	print()
	for i in range(0, sz-1):
		print(nodes[path[sz - i - 1]].getConnectionDetail(Topic(path[sz-i-2])))
	process = psutil.Process(os.getpid())
	print((process.memory_info().rss)/ (1000 * 1000), 'mb of memory used.')
	elapsedTime = timeit.default_timer() - startTime
	val = "{0:.2f}".format((elapsedTime / 60.0))
	print('Searched in', val, 'minutes.')

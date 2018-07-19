from Graph.TopicNode import TopicNode
from Graph.Topic import Topic
from Graph.GraphManager import GraphManager
from BSHelpers.SourceElement import SourceElement
import timeit, sys, codecs

from functools import partial
from itertools import repeat
from multiprocessing import Pool, freeze_support # This is a thread-based Pool
from multiprocessing import cpu_count

aylmao = []

def test(a):
	aylmao.append(a)


if __name__ == '__main__':
	d = [1,2,3,4,5,6,7,8,9]
	pool = Pool(cpu_count() * 2)
	pool.map(test, d)

	print(aylmao)
	#pool = Pool(cpu_count() * 2)  # Creates a Pool with cpu_count * 2 threads.
	#startingLink = input('Enter the name of the starting link: ')
	depth = input('Enter the depth you want the tree to expand to: ')
	startTime = timeit.default_timer()
	print('Beginning expansion...')

	#GraphManager.readGraph();
	GraphManager.beginSearch(TopicNode(Topic('Mathematics')), 0, (int)(depth))
	#uh = GraphManager.beginSearchPooled(TopicNode(Topic('Mathematics')), (int)(depth))
	#GraphManager.dive();
	GraphManager.saveGraphPooled(uh);


	elapsedTime = timeit.default_timer() - startTime
	val = "{0:.2f}".format((elapsedTime / 60.0))
	print('Created a',depth, 'deep search in ',val , 'minutes.')

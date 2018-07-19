from Graph.TopicNode import TopicNode
from Graph.Topic import Topic
from Graph.GraphManager import GraphManager
from BSHelpers.SourceElement import SourceElement
import timeit, sys, codecs

from functools import partial
from itertools import repeat
from multiprocessing import Pool, freeze_support # This is a thread-based Pool
from multiprocessing import cpu_count

if __name__ == '__main__':

	#pool = Pool(cpu_count() * 2)  # Creates a Pool with cpu_count * 2 threads.
	#startingLink = input('Enter the name of the starting link: ')
	depth = input('Enter the depth you want the tree to expand to: ')
	startTime = timeit.default_timer()
	print('Beginning expansion...')

	#GraphManager.readGraph();
	GraphManager.beginSearch(TopicNode(Topic('Measure_(mathematics)')), 0, (int)(depth))
	#GraphManager.beginSearchPooled(TopicNode(Topic('Mathematics')), (int)(depth))
	#GraphManager.dive();
	GraphManager.saveGraph();


	elapsedTime = timeit.default_timer() - startTime
	val = "{0:.2f}".format((elapsedTime / 60.0))
	print('Created a',depth, 'deep search in ',val , 'minutes.')

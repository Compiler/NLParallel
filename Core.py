from Graph.TopicNode import TopicNode
from Graph.Topic import Topic
from Graph.GraphManager import GraphManager
from BSHelpers.SourceElement import SourceElement
import timeit, sys, codecs


if __name__ == '__main__':
	depth = input('Enter the depth you want the tree to expand to: ')
	startTime = timeit.default_timer()
	print('Beginning expansion...')

	graphManager = GraphManager()
	graphManager.p_beginSearch(TopicNode(Topic('Mathematics')), (int)(depth))
	graphManager.saveGraph('tester');


	elapsedTime = timeit.default_timer() - startTime
	val = "{0:.2f}".format((elapsedTime / 60.0))
	print('Created a',depth, 'deep search in ',val , 'minutes.')

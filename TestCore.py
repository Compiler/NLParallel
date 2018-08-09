from Graph.TopicNode import TopicNode
from Graph.Topic import Topic
from Graph.GraphManager import GraphManager
from BSHelpers.SourceElement import SourceElement
import timeit, sys, codecs, pickle, os, psutil
from Search.SearchUtils import SearchUtils
from FileWriters.GraphWriter import GraphWriter


if __name__ == '__main__':
	for k in range(2, 4):
		for i in range(0, 21):
			startTime = timeit.default_timer()

			chunkSize = 50 * i
			graphManager = GraphManager()
			graphManager.p_beginSearch(TopicNode(Topic('Mathematics')), k, chunkSize)



			elapsedTime = timeit.default_timer() - startTime
			val = "{0:.2f}".format((elapsedTime / 60.0))
			print('Populated',k,'deep graph in', val, 'minutes using chunk size:', chunkSize)

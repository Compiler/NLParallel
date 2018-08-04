from Graph.TopicNode import TopicNode
from Graph.Topic import Topic
from Graph.GraphManager import GraphManager
from BSHelpers.SourceElement import SourceElement
import timeit, sys, codecs, pickle, os, psutil
from Search.SearchUtils import SearchUtils
from FileWriters.GraphWriter import GraphWriter


if __name__ == '__main__':

	startTime = timeit.default_timer()

	nodes = pickle.load(open('GraphData/p4_graphNodes.p', "rb"))

	#GraphWriter.writeSIFGraph(nodes, 'graphBrain_' + str(i))







	elapsedTime = timeit.default_timer() - startTime
	val = "{0:.2f}".format((elapsedTime / 60.0))
	print('Populated graph in', val, 'minutes.')

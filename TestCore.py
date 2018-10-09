from Graph.TopicNode import TopicNode
from Graph.Topic import Topic
from Graph.GraphManager import GraphManager
from BSHelpers.SourceElement import SourceElement
import timeit, sys, codecs, pickle, os, psutil
from Search.SearchUtils import SearchUtils
from FileWriters.GraphWriter import GraphWriter


if __name__ == '__main__':


	startTime = timeit.default_timer()

	graphManager = GraphManager()
	graphManager.p_beginSearch(TopicNode(Topic('Mathematics')), 2, True)



	elapsedTime = timeit.default_timer() - startTime
	val = "{0:.2f}".format((elapsedTime / 60.0))

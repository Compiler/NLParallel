from Graph.TopicNode import TopicNode
from Graph.Topic import Topic
from Graph.GraphManager import GraphManager
import timeit, sys




if __name__ == '__main__':


	#startingLink = input('Enter the name of the starting link: ')
	depth = input('Enter the depth you want the tree to expand to: ')
	startTime = timeit.default_timer()
	print('Beginning expansion...')

	topicNode = TopicNode(Topic('mathematics'))
	GraphManager.beginSearch(topicNode, (int)(depth))


	elapsedTime = timeit.default_timer() - startTime
	val = "{0:.2f}".format((elapsedTime / 60.0))
	print('Created a',depth, 'deep search in ',val , 'minutes.')

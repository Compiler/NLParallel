import sys, re,urllib,requests, codecs, operator, gzip, timeit, io

class WebTool:
	parser = 'lxml'

	#Gets the html of the page given end half of url (just the topic)
	#THIS REQUIRES PINGING NETWORK
	def getTopicSourceCode(topic: str):
	    opener = urllib.request.build_opener()
	    opener.addheaders = [('User-agent', 'MyTestScript/1.0 (contact at myscript@mysite.com)'), ('Accept-encoding', 'gzip')]
	    resource = opener.open("http://en.wikipedia.org/wiki/" + topic)
	    if resource.info().get('Content-Encoding') == 'gzip':
	        return gzip.GzipFile(fileobj=io.BytesIO( resource.read())).read()
	    else:
	        return resource.read()

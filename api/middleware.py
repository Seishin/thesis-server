class ContentTypeMiddleware(object):

	def process_request(self, request):

	    if request.method in ('POST', 'GET'):
	    	# request.META['CONTENT_TYPE'] = 'application/x-www-form-urlencoded'
	    	pass
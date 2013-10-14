from django.conf.urls import patterns, include, url
from piston.resource import Resource
from api.handlers import *

profile_info_handler = Resource(ProfileInfoHandler)
profile_marks_handler = Resource(ProfileMarksHandler)
profile_auth_handler = Resource(ProfileAuthHandler)

urlpatterns = patterns('',
	url(r'^profile/$', profile_info_handler, { 'emitter_format': 'json' }),
	url(r'^marks/$', profile_marks_handler, { 'emitter_format': 'json' }),
	url(r'^auth/$', profile_auth_handler, { 'emitter_format': 'json' }),
	)
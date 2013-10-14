from django.contrib import auth
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.csrf import csrf_exempt
from piston.handler import BaseHandler
from profiles.models import *
from piston.utils import rc

import base64

class ProfileInfoHandler(BaseHandler):
	allowed_methods = ('GET',)

	def read(self, request):

		if 'HTTP_TOKEN' and 'HTTP_USER' in request.META:
			token = request.META['HTTP_TOKEN']
			username = request.META['HTTP_USER']

			user = Profile.objects.get(username = username)

			if user is not None:
				if default_token_generator.check_token(user, token):
					profile = Student.objects.get(id = user.student_id)
					faculty = Faculty.objects.get(id = profile.faculty_id)
					major = Major.objects.get(id = profile.major_id)

					response = {
							'username' : user.username, 
							'email' : user.email, 
							'first_name' : profile.first_name, 
							'last_name' : profile.last_name, 
							'pin' : profile.pin, 
							'birth_date' : profile.birth_date, 
							'nationality' : profile.nationality,
							'faculty_number' : profile.faculty_number, 
							'major' : major.title,
							'faculty' : faculty.title, 
							'degree' : profile.get_degree_display(),
							'status' : profile.get_status_display(),
							'year' : profile.year
						}
					

					return response
				else:
					return rc.FORBIDDEN
			else:
				return rc.FORBIDDEN
		else:
			return rc.FORBIDDEN

class ProfileMarksHandler(BaseHandler):
	allowed_methods = ('GET')

	@csrf_exempt
	def read(self, request):

		if 'HTTP_TOKEN' and 'HTTP_USER' in request.META:
			token = request.META['HTTP_TOKEN']
			username = request.META['HTTP_USER']

			user = Profile.objects.get(username = username)

			if user is not None:
				if default_token_generator.check_token(user, token):
					profile = Student.objects.get(id = user.student_id)
					marks = Mark.objects.filter(student = profile.id)

					response = []

					for mark in marks:
						response.append(
							{
								'title' : mark.title, 
								'mark' : mark.get_mark_display(), 
								'date' : mark.date, 
								'form_of_control' : mark.get_form_of_control_display(),
								'year' : mark.year, 
								'semester' : mark.semester, 
							}
						)

					return response
				else:
					return rc.FORBIDDEN
			else:
				return rc.FORBIDDEN
		else:
			return rc.FORBIDDEN

		

class ProfileAuthHandler(BaseHandler):
	allowed_methods = ('GET', 'POST',)

	def read(self, request):

		if 'HTTP_AUTHORIZATION' in request.META:
				auth_data = request.META['HTTP_AUTHORIZATION'].split()
				if len(auth_data) == 2:
					if auth_data[0].lower() == "basic":
						username, password = base64.b64decode(auth_data[1]).split(':')

						user = auth.authenticate(username=username, password=password)
						if user is not None:
							if user.is_active:
								auth.login(request, user)

								return {"token" : default_token_generator.make_token(user)}
						else:
							return rc.FORBIDDEN
		else:
			return rc.FORBIDDEN
	
	@csrf_exempt
	def create(self, request):

		if 'HTTP_USER' in request.META and 'HTTP_TOKEN' in request.META:
			user = Profile.objects.get(username = request.META['HTTP_USER'])

			if default_token_generator.check_token(user, request.META['HTTP_TOKEN']):
				return rc.ALL_OK
			else:
				return rc.FORBIDDEN
		else:
			return rc.FORBIDDEN
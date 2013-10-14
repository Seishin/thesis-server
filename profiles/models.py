# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.encoding import force_unicode


class Student(models.Model):
	first_name		= models.CharField(max_length=20, null=False)
	last_name		= models.CharField(max_length=20, null=False)

	pin 			= models.DecimalField(max_digits=10, decimal_places=0, unique=True, null=True)
	birth_date 		= models.DateField(null=True)
	nationality 	= models.CharField(max_length=30, null=True)


	STATUS_CHOICES = (('1', u'Семестриално незавършил'),
						('2', u'Семестриално завършил'))

	DEGREE_CHOICES = (('1', u'Бакалавър'),
						('2', u'Магистър'),
						('3', u'Доктор'))

	faculty_number 	= models.DecimalField(max_digits=10, decimal_places=0, unique=True, null=False)
	faculty 		= models.ForeignKey('Faculty', null=True)	
	major			= models.ForeignKey('Major', null=True)
	degree			= models.CharField(max_length=20, choices=DEGREE_CHOICES, default=1)
	status			= models.CharField(max_length=20, choices=STATUS_CHOICES, default=1)
	year			= models.IntegerField(null=True)

	def __unicode__(self):
		return force_unicode(self.first_name + ' ' + self.last_name)

class Faculty(models.Model):

	title 	= models.CharField(max_length = 50, unique = True, null = False)
	address = models.CharField(max_length = 100)

	def __unicode__(self):
		return force_unicode(self.title) 

class Major(models.Model):

	title 	= models.CharField(max_length = 50, unique = True, null = False)

	def __unicode__(self):
		return force_unicode(self.title)

class Mark(models.Model):

	MARK_CHOICES = (
					('1', u'Слаб (2)'),
					('2', u'Среден (3)'),
					('3', u'Добър (4)'),
					('4', u'Мн. Добър (5)'),
					('5', u'Отличен (6)'))

	FORM_OF_CONTROL_CHOICES = (
								('1', u'Изпит'),
								('2', u'Текуща оценка'),
								('3', u'Заверка'))
	
	title			= models.CharField(max_length = 50, null = False)
	mark 			= models.CharField(max_length = 20, choices = MARK_CHOICES, default = 1)
	semester		= models.IntegerField()
	year			= models.IntegerField()
	form_of_control = models.CharField(max_length = 10, choices = FORM_OF_CONTROL_CHOICES, default = 1)
	date 			= models.DateField()

	student   		= models.ForeignKey('Student')

	def __unicode__(self):
		return force_unicode(self.title)

class ProfileManager(BaseUserManager):

	def create_user(self, username, email, password, faculty_number):

		user = self.model(username = username, email = email, 
			faculty_number = Student.objects.get(faculty_number = faculty_number))
		user.set_password(password)

		user.save()

		return user

	def create_superuser(self, username, email, password):

		user = self.model(username = username, email = email)
		user.set_password(password)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save()

		return user

class Profile(AbstractUser):
	student = models.OneToOneField(Student, null = True)

	REQUIRED_FIELDS = ['email']

	objects = ProfileManager()

	def get_profile(self):
		return self.student

	def get_marks(self):
		return Mark.objects.filter(student = self.student)

	def __unicode__(self):
		return force_unicode(self.get_username())
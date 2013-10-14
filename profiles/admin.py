from django.contrib import admin
from profiles.models import *

admin.site.register(Profile)
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Major)
admin.site.register(Mark)
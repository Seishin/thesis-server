from django.test import TestCase
from django.test.client import RequestFactory

class GetUserProfileTest(TestCase):
    
    def setUp(self):
    	self.factory = RequestFactory()

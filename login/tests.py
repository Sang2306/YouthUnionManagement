from django.test import TestCase
from .models import User
# Create your tests here.
class TestUserModel(TestCase):
    @classmethod
    def setUpTestData(self):
        """
            Run truoc khi thuc hien cac test function
            setup du lieu cho cac test function
        """
        self.user = User('N16DCCN131', 'D16CQCN03-N', 'Le Tanh Sang', '1998-23-06', 1, 'sakdhksdk', 60)
    
    def test_user_info(self):
        self.assertTrue(len(self.user.user_ID) <= 12)
        self.assertTrue(len(self.user.name) <= 25)
        self.assertTrue(len(self.user.class_ID) <= 12)
    
    def test_accumulated_point(self):
        self.assertTrue(self.user.accumulated_point <= 100)
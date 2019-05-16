from django.test import TestCase
from login.models import User, Activity
from django.utils import timezone
# Create test models here
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
        self.user.refresh_accumulated_point()
        self.assertTrue(self.user.accumulated_point <= 100)
    
    def test_set_new_password(self):
        new_password = '3879hsfu89'
        self.user.set_new_password(new_password)
        self.assertTrue(self.user.password == new_password)

class TestActivityModel(TestCase):
    @classmethod
    def setUpTestData(self):
        self.activity = Activity.objects.create(
            activity_ID=6374,
            name='TEST ACTIVITY',
            organizers='I am the owner so i hope you are doing good @LTS',
            start_date=timezone.now(),
            semester=1,
            description='NO',
            point=3,
            number_of_register=534
        )
    
    def test_is_opening(self):
        self.assertTrue(self.activity.is_opening())
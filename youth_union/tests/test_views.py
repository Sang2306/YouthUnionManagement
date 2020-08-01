from django.test import Client, TestCase
from django.urls import reverse
from login.models import User, Role
# Create test views here

class TestViews(TestCase):
    @classmethod
    def setUpTestData(self):
        self.client = Client()
        self.login_url = reverse('youth_union:login')
        self.personal_url = reverse('youth_union:personal')
        self.exit_url = reverse('youth_union:exit')
        self.activities_url = reverse('youth_union:activities')
        self.upload_url = reverse('youth_union:upload')

    def test_login_view(self):
        response = self.client.get(self.login_url)
        self.assertEquals(response.status_code, 200)

    def test_personal_view(self):
        response = self.client.get(self.personal_url)
        self.assertEquals(response.status_code, 302)

    def test_exit_view(self):
        response = self.client.get(self.exit_url)
        self.assertEquals(response.status_code, 302)
    
    def test_upload_view(self):
        response = self.client.get(self.upload_url)
        self.assertEquals(response.status_code, 302)
    
    def test_activities_view(self):
        response = self.client.get(self.activities_url)
        self.assertEquals(response.status_code, 302)

class TestLoginView(TestCase):
    @classmethod
    def setUpTestData(self):
        self.client = Client()
        self.login_url = reverse('youth_union:login')
        role = Role.objects.create(
            role_ID=1,
            role_name='Sinh vien',
        )
        self.user = User.objects.create(
            user_ID='N16DCCN131',
            class_ID='D16CQCN03',
            name='LE TANH SANG',
            date_of_birth='1998-06-23',
            role=role,
            password='idontknow', 
        )
    
    def test_login_is_succeed(self):
        response = self.client.post(self.login_url, {
            'ID':self.user.user_ID,
            'password':self.user.password,
        })
        print(response)
        self.assertEquals(response.status_code, 302)
        self.assertTrue(response.url=='/home/')
        
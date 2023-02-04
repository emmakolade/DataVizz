from django.urls import reverse
from rest_framework.test import APITestCase
from ..models import DataFile


class TestSetup(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.upload_url = reverse('upload')
        self.queryset = DataFile.objects.all()

        self.user_data = {
            'username': 'Kolade',
            'password': 'password123#',
            'email': 'kolade@gmail.com',

        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

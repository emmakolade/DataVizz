from django.urls import reverse
from rest_framework.test import APITestCase


class TestSetup(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')

        self.user_data = {
            'username': 'Kolade',
            'password': 'password123#',
            # 'full_name': 'KoladeOlanipekun',
            'email': 'kolade@gmail.com',

        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

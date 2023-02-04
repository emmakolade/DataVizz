from .test_setup import TestSetup
from rest_framework import status
from ..models import User


class TestViews(TestSetup):

    def test_user_must_register_with_data(self):
        '''
        ensures user cannot create account with no data provided 
        '''
        response = self.client.post(self.register_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_if_user_can_register(self):
        '''
        ensure users can register succesfully
        '''
        response = self.client.post(
            self.register_url, self.user_data, format='json')
        self.assertEqual(response.data['email'], self.user_data['email'])
        self.assertEqual(response.data['username'], self.user_data['username'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_if_user_can_login(self):

        res = self.client.post(
            self.register_url, self.user_data, format='json')
        # import pdb; pdb.set_trace()
        username = res.data['username']
        user = User.objects.get(username=username)
        user.is_active = True
        user.save()
        response = self.client.post(
            self.login_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_if_user_has_the_right_login_credential(self):
        response = self.client.post(
            self.login_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

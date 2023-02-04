from .test_setup import TestSetup
from rest_framework import status
from ..models import User
from ..serializers import DataFileSerializer
from ..models import DataFile


class TestView(TestSetup):

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

    def auth(self):
        self.client.post(
            self.register_url, self.user_data)
        response = self.client.post(
            self.login_url, self.user_data)
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer{access_token}")

    def test_should_not_allow_upload_for_user_with_no_auth(self):
        data = {'file': 'fakefile.csv'}
        res = self.client.post(
            self.upload_url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_not_allow_upload_for_user_with_no_auth(self):
        self.auth()
        data = {'file': 'fakefile.csv'}
        res = self.client.post(
            self.upload_url, data, format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_should_allow_auth_user_upload_file(self):
        
    #     self.auth()
    #     data = {'file': 'fakefile.csv'}
    #     res = self.client.post(
    #         self.upload_url, data, format='json')
    #     # serializer = DataFileSerializer(data)
    #     # self.assertTrue(serializer.is_valid())
    #     # self.perform_create(serializer)
    #     self.assertEqual(DataFile.objects.count(), 1)
    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)

# class TestViewsData(TestSetupData):

#     def test_should_not_allow_upload_for_user_with_no_auth(self):
#         data = {'file': 'fakefile.csv'}
#         res = self.client.post(
#             self.upload_url, data, format='json')
#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # self.assertRaises(serializer.ValidationError)

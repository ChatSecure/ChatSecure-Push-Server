from __future__ import absolute_import
from rest_framework.test import APITestCase

ACCOUNTS_URL = '/api/v1/accounts/'

def maybe_is_uuid(potential_uuid):
    return potential_uuid is not None and len(potential_uuid) == 36


def maybe_is_auth_token(potential_uuid):
    return potential_uuid is not None and len(potential_uuid) == 40


class AccountTests(APITestCase):
    def test_create_account_no_email(self):
        """
        Ensure we can create a new account and subsequently login without email
        """

        data = {'username': u'jackRuby', 'password': u'dallas4life'}
        self.check_signup_then_login(data)


    def test_create_account_with_email(self):
        """
        Ensure we can create a new account and subsequently login with email
        """

        data = {'username': u'jackRuby', 'email': u'redjack@earthlink.net', 'password': u'dallas4life'}
        self.check_signup_then_login(data)


    def test_password_auth(self):
        data = {'username': u'jackRuby', 'password': u'dallas4life'}

        response = self.client.post(ACCOUNTS_URL, data)
        self.check_account_resp(data, response)

        data['password'] = u'blah'
        response = self.client.post(ACCOUNTS_URL, data)
        self.assertTrue(response.status_code == 401, "Login with incorrect password is unauthorized")
        self.assertTrue('error' in response.data, "Error response contains error")
        self.assertTrue('username' not in response.data, "Error response omits username")
        self.assertTrue('token' not in response.data, "Error response omits token")
        self.assertTrue('password' not in response.data, "Error response omits password")

    # Utility methods requiring assertions

    def check_signup_then_login(self, request_data):
        '''
        Test whether account creation then login return expected responses
        :param request_data: create account request data including a 'username' and 'password' key at minimum
        '''

        create_response = self.client.post(ACCOUNTS_URL, request_data)
        self.check_account_resp(request_data, create_response)

        login_response = self.client.post(ACCOUNTS_URL, request_data)
        self.check_account_resp(request_data, login_response)

    def check_account_resp(self, request_data, response):
        self.assertTrue(200 <= response.status_code < 300, 'Response was successful')

        # Assert presence of required response fields
        self.assertTrue(response.data['username'] == request_data['username'], 'Response has expected username')
        self.assertTrue(maybe_is_uuid(response.data.get('id', None)), 'Response has expected id')
        self.assertTrue(maybe_is_auth_token(response.data.get('token', None)), 'Response has expected token')

        # Assert absence of no-no response fields
        self.assertTrue('password' not in response.data, 'Response omits password')

        # Assert conditional fields
        if 'email' in request_data:
            self.assertTrue(response.data.get('email', None) == request_data['email'], 'Response has email')
        else:
            self.assertTrue(len(response.data.get('email', '')) == 0, 'Response omits blank email')


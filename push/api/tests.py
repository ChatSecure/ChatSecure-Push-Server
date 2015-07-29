from rest_framework.test import APITestCase

ACCOUNTS_URL = '/api/v1/accounts/'
APNS_DEVICE_URL = '/api/v1/device/apns/'
GCM_DEVICE_URL = '/api/v1/device/gcm/'
TOKEN_URL = '/api/v1/tokens/'


class ApiIntegrationTests(APITestCase):
    def test_device_and_token_visibility(self):
        '''
        Ensure that ownership permissions are respected for tokens and devices
        e.g: Alice's Devices and Tokens are not visible to Bob
        '''

        alice_acct_resp = self.create_account(username=u'alice', password=u'asdf1234')
        alice_auth_token = alice_acct_resp.data['token']
        alice_device_resp = self.create_device(name='alice_iPhone', registration_id='1234asdf',
                                               auth_token=alice_auth_token)
        alice_token_resp = self.create_token(name=u"alice token", device_id=alice_device_resp.data['id'],
                                             auth_token=alice_auth_token)

        bob_acct_resp = self.create_account(username=u'bob', password=u'jkl;')
        bob_auth_token = bob_acct_resp.data['token']
        bob_device_registration_id = u"12345jkl;"
        bob_device_resp = self.create_device(name=u"bob's Android", registration_id=bob_device_registration_id,
                                             auth_token=bob_auth_token, apns=False)
        bob_token_resp = self.create_token(name=u"bob token", device_id=bob_device_resp.data['id'],
                                           auth_token=bob_auth_token, apns=False)

        bob_devices_resp = self.get_devices(auth_token=bob_auth_token, apns=False)
        self.assertTrue(bob_devices_resp.data['count'] == 1, 'Bob device list is correct length')
        self.assertTrue(bob_devices_resp.data['results'][0]['registration_id'] == bob_device_registration_id,
                        'Returned Bob device has expected registration id')

        bob_tokens_resp = self.get_tokens(bob_auth_token)
        self.assertTrue(bob_tokens_resp.data['count'] == 1, 'Bob token list is correct length')
        self.assertTrue(bob_tokens_resp.data['results'][0]['token'] == bob_token_resp.data['token'],
                        'Returned Bob token has expected token value')

    def create_account(self, username, password):
        resp = self.client.post(ACCOUNTS_URL, {'username': username, 'password': password})
        self.assertTrue(200 <= resp.status_code < 300, 'Create account response successful')
        self.assertTrue(resp.data.get('token', None) is not None, 'Create account response has auth token')
        return resp

    def create_device(self, name, registration_id, auth_token, apns=True):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + auth_token)
        resp = self.client.post(APNS_DEVICE_URL if apns else GCM_DEVICE_URL,
                                {'name': name, 'registration_id': registration_id})
        self.assertTrue(200 <= resp.status_code < 300, 'Create device response successful')
        return resp

    def create_token(self, name, device_id, auth_token, apns=True):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + auth_token)
        device_key = 'apns_device' if apns else 'gcm_device'
        resp = self.client.post(TOKEN_URL, {'name': name, device_key: device_id})
        self.assertTrue(200 <= resp.status_code < 300, 'Create token response successful')
        return resp

    def get_devices(self, auth_token, apns=True):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + auth_token)
        resp = self.client.get(APNS_DEVICE_URL if apns else GCM_DEVICE_URL)
        self.assertTrue(200 <= resp.status_code < 300, 'Get device response successful')
        return resp

    def get_tokens(self, auth_token):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + auth_token)
        resp = self.client.get(TOKEN_URL)
        self.assertTrue(200 <= resp.status_code < 300, 'Get device response successful')
        return resp

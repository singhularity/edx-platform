"""
Amplify OAuth2 Sign-in backends
"""

from social.backends.oauth import BaseOAuth2
import requests


class AmplifyOAuth2(BaseOAuth2):
    """Amplify OAuth authentication backend"""
    name = 'amplify-oauth2'
    REDIRECT_STATE = False
    AUTHORIZATION_URL = 'http://tmc241.mc.wgenhq.net/mobilelogin/oauth2/auth'
    ACCESS_TOKEN_URL = 'http://tmc241.mc.wgenhq.net/mobilelogin/oauth2/token'
    ACCESS_TOKEN_METHOD = 'POST'
    EXTRA_DATA = [
        ('expires_in', 'expires')
    ]

    def get_user_id(self, details, response):
        """Use user uid as unique id"""
        return response['user_uid']

    def auth_params(self, state=None):
        client_id, _ = self.get_key_and_secret()
        params = {
            'client_id': client_id
        }
        if self.STATE_PARAMETER and state:
            params['state'] = state
        if self.RESPONSE_TYPE:
            params['response_type'] = self.RESPONSE_TYPE
        return params

    def get_user_details(self, response):
        """Return user details from Amplify account"""
        return {'username': response.get('user_uid', ''),
                'email': response.get('email', ''),
                'fullname': response.get('name', '')}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        headers = {'Cookie': 'sso.auth_token=' + access_token}
        response = requests.get("http://tmc241.mc.wgenhq.net/mobilelogin/gatekeeper", headers=headers)
        try:
            return response.json()
        except ValueError:
            return None

    def auth_html(self):
        """Return login HTML content returned by provider
            It is not being used, just override the abstract class to pass the quality tests
        """
        pass

"""
Amplify OAuth2 Sign-in backends
"""

from social.backends.oauth import BaseOAuth2
import json
import urllib2


class AmplifyOAuth2(BaseOAuth2):
    """Amplify OAuth authentication backend"""
    name = 'amplify'
    REDIRECT_STATE = False
    AUTHORIZATION_URL = 'https://mclasshome.com/mobilelogin/oauth2/auth'
    ACCESS_TOKEN_URL = 'https://mclasshome.com/mobilelogin/oauth2/token'
    ACCESS_TOKEN_METHOD = 'POST'
    EXTRA_DATA = [
        ('refresh_token', 'refresh_token', True),
        ('expires_in', 'expires'),
        ('token_type', 'token_type', True)
    ]

    def get_user_id(self, details, response):
        """Use user uid as unique id"""
        return response['user_uid']

    def auth_params(self, state=None):
        client_id, client_secret = self.get_key_and_secret()
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
        opener = urllib2.build_opener()
        opener.addheaders.append(('Cookie', 'sso.auth_token='+access_token))
        url = opener.open("https://mclasshome.com/mobilelogin/gatekeeper")
        try:
            return json.load(url)
        except ValueError:
            return None

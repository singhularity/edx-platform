"""
Amplify OAuth2 Sign-in backends
Refer to this documentation: http://psa.matiasaguirre.net/docs/backends/implementation.html#oauth
"""

from social.backends.oauth import BaseOAuth2
import requests


class AmplifyOAuth2(BaseOAuth2):
    """Amplify OAuth authentication backend"""
    #: The name defines the backend name and identifies it during the auth process.
    # The name is used in the redirect_uri auth/complete/<backend name> .
    name = 'amplify'

    #: For those providers that do not recognise the state parameter,
    # the app can add a redirect_state argument to the redirect_uri to mimic it.
    REDIRECT_STATE = False

    #: This is the entry point for the authorization mechanism.
    # We need to change it to "https://mclasshome.com/mobilelogin/oauth2/auth"
    AUTHORIZATION_URL = 'http://tmc241.mc.wgenhq.net/mobilelogin/oauth2/auth'

    #: This must point to the API endpoint that provides an access_token
    # needed to authenticate in users behalf on future API calls.
    ACCESS_TOKEN_URL = 'http://tmc241.mc.wgenhq.net/mobilelogin/oauth2/token'
    ACCESS_TOKEN_METHOD = 'POST'

    #: During the auth process some basic user data is returned by the provider or retrieved
    # by user_data() method which usually is used to call some API on the provider to retrieve it.
    # This data will be stored under UserSocialAuth.extra_data attribute, but to make it
    # accessible under some common names on different providers, this attribute defines a list of
    # tuples in the form (name, alias) where name is the key in the user data (which should be
    # a dict instance) and alias is the name to store it on extra_data.
    EXTRA_DATA = [
        ('expires_in', 'expires')
    ]

    def get_user_id(self, details, response):
        """Use user uid as unique id"""
        return response['user_uid']

    def get_redirect_uri(self, state=None):
        """Build redirect with redirect_state parameter."""
        uri = self.redirect_uri
        #: This is a hack to change http to https, we need to
        # figure out a better way of doing it.
        if 'amplifyedx.developer.com' in uri:
            uri = uri.replace('http', 'https')
        if self.REDIRECT_STATE and state:
            uri = url_add_parameters(uri, {'redirect_state': state})
        return uri

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
        return {'username': response.get('user_uid', '')}

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

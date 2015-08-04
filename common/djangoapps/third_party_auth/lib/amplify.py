"""
Amplify OAuth2 Sign-in backends
Refer to this documentation: http://psa.matiasaguirre.net/docs/backends/implementation.html#oauth
"""

from social.backends.oauth import BaseOAuth2, BaseAuth, OAuthAuth
from social.utils import url_add_parameters
import requests
from django.conf import settings
from third_party_auth.lib.search_napi import napi_main
from concurrent import futures


def overrides(interface_class):
    """overrides decorator"""
    def overrider(method):
        """
        This will check that the class given as a parameter has the
        same method (or something) name as the method being decorated.
        """
        assert method.__name__ in dir(interface_class)
        return method
    return overrider


class AmplifyOAuth2(BaseOAuth2):
    """Amplify OAuth authentication backend"""
    #: The name defines the backend name and identifies it during the auth process.
    # The name is used in the redirect_uri auth/complete/<backend name> .
    name = settings.FEATURES.get('AMPLIFY_AUTH_NAME')

    #: For those providers that do not recognise the state parameter,
    # the app can add a redirect_state argument to the redirect_uri to mimic it.
    REDIRECT_STATE = settings.FEATURES.get('AMPLIFY_REDIRECT_STATE')

    #: This is the entry point for the authorization mechanism.
    # We need to change it to "https://mclasshome.com/mobilelogin/oauth2/auth"
    AUTHORIZATION_URL = settings.FEATURES.get('AMPLIFY_AUTHORIZATION_URL')

    #: This must point to the API endpoint that provides an access_token
    # needed to authenticate in users behalf on future API calls.
    ACCESS_TOKEN_URL = settings.FEATURES.get('AMPLIFY_ACCESS_TOKEN_URL')
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

    @overrides(BaseAuth)
    def get_user_id(self, details, response):
        """Use user uid as unique id"""
        return response['user_uid']

    @overrides(BaseOAuth2)
    def get_redirect_uri(self, state=None):
        """Build redirect with redirect_state parameter."""
        uri = self.redirect_uri
        #: This is a hack to change http to https, we need to
        # figure out a better way of doing it.
        if 'http://amplifyedx.developer.com' in uri:
            uri = uri.replace('http', 'https')
        if self.REDIRECT_STATE and state:
            uri = url_add_parameters(uri, {'redirect_state': state})
        return uri

    @overrides(BaseOAuth2)
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

    @overrides(BaseAuth)
    def get_user_details(self, response):
        """Return user details from Amplify account"""
        username = response.get('username')
        name = response.get('name')
        email = response.get('email')
        return {'username': username,
                'email': email,
                'name': name,
                'honor_code': u'true',
                'terms_of_service': u'true'}

    @overrides(OAuthAuth)
    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        response_url = settings.FEATURES.get('AMPLIFY_RESPONSE_URL')
        headers = {'Cookie': 'sso.auth_token=' + access_token}
        response = requests.get(response_url, headers=headers)
        try:
            response_json = response.json()
            try:
                user_details = self.call_webapps(access_token, response_json.get('staff_uid'))[0][0]
                response_json['name'] = user_details.get('first_name') + " " + user_details.get('last_name')
                response_json['username'] = user_details.get('first_name') + "_" + user_details.get('last_name')
                response_json['email'] = user_details.get('email_address')
            #pylint: disable=broad-except
            except Exception:
                return None
            return response_json
        except ValueError:
            return None

    @overrides(BaseAuth)
    def auth_html(self):
        """Return login HTML content returned by provider
            It is not being used, just override the abstract class to pass the quality tests
        """
        pass

    def call_webapps(self, access_token, staff_uid):
        """Return napi details by webapps call"""
        napi_settings = settings.FEATURES.get('AMPLIFY_NAPI_SETTINGS')
        with futures.ThreadPoolExecutor(max_workers=1) as executor:
            webcall = [executor.submit(napi_main, access_token, napi_settings, None, staff_uid=staff_uid)]

            futures.wait(webcall)
            napi_details = webcall[0].result()
            return napi_details

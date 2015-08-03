import json
from django.shortcuts import redirect

__author__ = 'ssingh'

# import the User object
from django.conf import settings
from django.contrib.auth.models import User
import requests
from social.backends.oauth import BaseAuth

class LearningAuth(BaseAuth):

    # Create an authentication method
    # This is called by the standard Django login procedure

    name = 'LearningAuth'

    EXTRA_DATA = [
        ('expires_in', 'expires')
    ]

    def get_user_id(self, details, response):
        """Use user uid as unique id"""
        return response['user_uid']

    def authenticate(self, username=None, password=None, request=None):
        try:
            # Check if this user is valid on the mail server
            cookieStr = ""
            for cookie in request.COOKIES.keys():
                cookieStr += "{}={};".format(cookie, request.COOKIES.get(cookie))
            headers = {'Cookie': cookieStr}
            r = requests.get(settings.FEATURES["AMPLIFY_LEARNING_AUTH_STATUS_URL"], headers=headers, verify=False)
            if r.status_code != 200:
                return redirect("/register")
        except:
            if username is '':
                return redirect("/register")
            else:
                return None
        try:
            # Check if the user exists in Django's local database
            userData = json.loads(r.text)
            user = User.objects.get(email=userData.get('user'))
        except User.DoesNotExist:
            # AUDIT_LOG.warning(
            # u'Login failed - user with username {username} has no social auth with backend_name {backend_name}'.format(
            #     username=r.get('user'), backend_name='LearningAuth'))
            return redirect('/learningauth')
        return user

    # Required for your backend to work properly - unchanged in most scenarios
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

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

    def auth_html(self):
        """Return login HTML content returned by provider
            It is not being used, just override the abstract class to pass the quality tests
        """
        pass

    def auth_complete(self, *args, **kwargs):
        pass

    def auth_url(self):
        return "http://local.amplify.com:8002/wg-curriculum/auth/sso/login?redirect_url=http://local.amplify.com:8000/auth/complete/LearningAuth"




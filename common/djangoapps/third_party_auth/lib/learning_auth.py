import json
from django.shortcuts import redirect

__author__ = 'ssingh'

# import the User object
from django.conf import settings
from django.contrib.auth.models import User
import requests

class LearningAuth():

    # Create an authentication method
    # This is called by the standard Django login procedure

    def authenticate(self, username=None, request=None, learning_auth=True):
        try:
            # Check if this user is valid on the mail server
            cookieStr = ""
            for cookie in request.COOKIES.keys():
                cookieStr += "{}={};".format(cookie, request.COOKIES.get(cookie))
            headers = {'Cookie': cookieStr}

            host = request.get_host()
            if 'local' in host or '127' in host or '0' in host:
                learning_url = "http://localhost:8000/dummyLearningService"
            else:
                learning_url = settings.FEATURES["AMPLIFY_LEARNING_URL"] + "status"

            r = requests.get(learning_url, headers=headers, verify=False)
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




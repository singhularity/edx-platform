import json
from django.shortcuts import redirect, render_to_response

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
            # Check if this user is a valid learning user
            cookieStr = ""
            for cookie in request.COOKIES.keys():
                cookieStr += "{}={};".format(cookie, request.COOKIES.get(cookie))
            headers = {'Cookie': cookieStr}

            # Hack around because we cannot read cookies on the amplify domain locally
            host = request.get_host()
            if 'local' in host or '127' in host or '0' in host:
                learning_url = "http://localhost:8000/dummyLearningService"
            else:
                learning_url = settings.FEATURES["AMPLIFY_LEARNING_URL"] + "status"
            # If the user is not logged in then send a redirect
            # This can probably be done in a better way, all we need is a non user return value
            r = requests.get(learning_url, headers=headers, verify=False)
            if r.status_code != 200:
                return redirect("/register")
        except:
            if username is '':
                return redirect("/register")
            else:
                return None
        try:
            # We got a proper response from Learning so get the user details
            userData = json.loads(r.text)
            # If the user is a student redirect to the error page
            if "ROLE_STUDENT" in userData.get("roles"):
                return redirect('/login_error')
            user = User.objects.get(email=userData.get('user'))
        except User.DoesNotExist:
            # The user is logging in for the first time, again send a non user value as return value
            return redirect('/learningauth')
        return user

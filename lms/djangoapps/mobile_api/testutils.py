"""
Test utilities for mobile API tests:

  MobileAPITestCase - Common base class with helper methods and common functionality.
     No tests are implemented in this base class.

  Test Mixins to be included by concrete test classes and provide implementation of common test methods:
     MobileAuthTestMixin - tests for APIs with mobile_view and is_user=False.
     MobileAuthUserTestMixin - tests for APIs with mobile_view and is_user=True.
     MobileCourseAccessTestMixin - tests for APIs with mobile_course_access and verify_enrolled=False.
     MobileEnrolledCourseAccessTestMixin - tests for APIs with mobile_course_access and verify_enrolled=True.
"""
# pylint: disable=no-member
import ddt
from mock import patch
from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse

from opaque_keys.edx.keys import CourseKey
from courseware.tests.factories import UserFactory

from student import auth
from student.models import CourseEnrollment

from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase
from xmodule.modulestore.tests.factories import CourseFactory
import unittest


class MobileAPITestCase(ModuleStoreTestCase, APITestCase):
    """
    Base class for testing Mobile APIs.
    Subclasses are expected to define REVERSE_INFO to be used for django reverse URL, of the form:
       REVERSE_INFO = {'name': <django reverse name>, 'params': [<list of params in the URL>]}
    They may also override any of the methods defined in this class to control the behavior of the TestMixins.
    """
    def setUp(self):
        super(MobileAPITestCase, self).setUp()
        self.course = CourseFactory.create(mobile_available=True)
        self.user = UserFactory.create()
        self.password = 'test'
        self.username = self.user.username

    def tearDown(self):
        super(MobileAPITestCase, self).tearDown()
        self.logout()

    def login(self):
        """Login test user."""
        self.client.login(username=self.username, password=self.password)

    def logout(self):
        """Logout test user."""
        self.client.logout()

    def enroll(self, course_id=None):
        """Enroll test user in test course."""
        CourseEnrollment.enroll(self.user, course_id or self.course.id)

    def unenroll(self, course_id=None):
        """Unenroll test user in test course."""
        CourseEnrollment.unenroll(self.user, course_id or self.course.id)

    def login_and_enroll(self, course_id=None):
        """Shortcut for both login and enrollment of the user."""
        self.login()
        self.enroll(course_id)

    def api_response(self, reverse_args=None, expected_response_code=200, **kwargs):
        """
        Helper method for calling endpoint, verifying and returning response.
        If expected_response_code is None, doesn't verify the response' status_code.
        """
        url = self.reverse_url(reverse_args, **kwargs)
        response = self.url_method(url, **kwargs)
        if expected_response_code is not None:
            self.assertEqual(response.status_code, expected_response_code)
        return response

    def reverse_url(self, reverse_args=None, **kwargs):  # pylint: disable=unused-argument
        """Base implementation that returns URL for endpoint that's being tested."""
        reverse_args = reverse_args or {}
        if 'course_id' in self.REVERSE_INFO['params']:
            reverse_args.update({'course_id': unicode(kwargs.get('course_id', self.course.id))})
        if 'username' in self.REVERSE_INFO['params']:
            reverse_args.update({'username': kwargs.get('username', self.user.username)})
        return reverse(self.REVERSE_INFO['name'], kwargs=reverse_args)

    def url_method(self, url, **kwargs):  # pylint: disable=unused-argument
        """Base implementation that returns response from the GET method of the URL."""
        return self.client.get(url)


class MobileAuthTestMixin(object):
    """
    Test Mixin for testing APIs decorated with mobile_view.
    """
    def test_no_auth(self):
        self.logout()
        self.api_response(expected_response_code=401)


class MobileAuthUserTestMixin(MobileAuthTestMixin):
    """
    Test Mixin for testing APIs related to users: mobile_view with is_user=True.
    """
    def test_invalid_user(self):
        self.login_and_enroll()
        self.api_response(expected_response_code=403, username='no_user')

    def test_other_user(self):
        # login and enroll as the test user
        self.login_and_enroll()
        self.logout()

        # login and enroll as another user
        other = UserFactory.create()
        self.client.login(username=other.username, password='test')
        self.enroll()
        self.logout()

        # now login and call the API as the test user
        self.login()
        self.api_response(expected_response_code=403, username=other.username)


@ddt.ddt
class MobileCourseAccessTestMixin(object):
    """
    Test Mixin for testing APIs marked with mobile_course_access.
    (Use MobileEnrolledCourseAccessTestMixin when verify_enrolled is set to True.)
    Subclasses are expected to inherit from MobileAPITestCase.
    Subclasses can override verify_success, verify_failure, and init_course_access methods.
    """
    ALLOW_ACCESS_TO_UNRELEASED_COURSE = False  # pylint: disable=invalid-name

    def verify_success(self, response):
        """Base implementation of verifying a successful response."""
        self.assertEqual(response.status_code, 200)

    def verify_failure(self, response):
        """Base implementation of verifying a failed response."""
        self.assertEqual(response.status_code, 404)

    def init_course_access(self, course_id=None):
        """Base implementation of initializing the user for each test."""
        self.login_and_enroll(course_id)

    def test_success(self):
        self.init_course_access()

        response = self.api_response(expected_response_code=None)
        self.verify_success(response)  # allow subclasses to override verification

    def test_course_not_found(self):
        non_existent_course_id = CourseKey.from_string('a/b/c')
        self.init_course_access(course_id=non_existent_course_id)

        response = self.api_response(expected_response_code=None, course_id=non_existent_course_id)
        self.verify_failure(response)  # allow subclasses to override verification

    @unittest.skip("US37379 - fix unit test")
    @patch.dict('django.conf.settings.FEATURES', {'DISABLE_START_DATES': False})
    def test_unreleased_course(self):
        self.init_course_access()

        response = self.api_response(expected_response_code=None)
        if self.ALLOW_ACCESS_TO_UNRELEASED_COURSE:
            self.verify_success(response)
        else:
            self.verify_failure(response)

    # A tuple of Role Types and Boolean values that indicate whether access should be given to that role.
    @ddt.data(
        (auth.CourseBetaTesterRole, True),
        (auth.CourseStaffRole, True),
        (auth.CourseInstructorRole, True),
        (None, False)
    )
    @ddt.unpack
    def test_non_mobile_available(self, role, should_succeed):
        self.init_course_access()

        # set mobile_available to False for the test course
        self.course.mobile_available = False
        self.store.update_item(self.course, self.user.id)

        # set user's role in the course
        if role:
            role(self.course.id).add_users(self.user)

        # call API and verify response
        response = self.api_response(expected_response_code=None)
        if should_succeed:
            self.verify_success(response)
        else:
            self.verify_failure(response)


class MobileEnrolledCourseAccessTestMixin(MobileCourseAccessTestMixin):
    """
    Test Mixin for testing APIs marked with mobile_course_access with verify_enrolled=True.
    """
    def test_unenrolled_user(self):
        self.login()
        self.unenroll()
        response = self.api_response(expected_response_code=None)
        self.verify_failure(response)

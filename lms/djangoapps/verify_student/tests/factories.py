"""
Factories related to student verification.
"""

from factory.django import DjangoModelFactory
from verify_student.models import SoftwareSecurePhotoVerification


# Factories are self documenting
# pylint: disable=missing-docstring
class SoftwareSecurePhotoVerificationFactory(DjangoModelFactory):
    """
    Factory for SoftwareSecurePhotoVerification
    """
    class Meta(object):
        model = SoftwareSecurePhotoVerification

    status = 'approved'

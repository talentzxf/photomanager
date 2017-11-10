import datetime

from django.test import TestCase
from django.utils import timezone


class ImageModelTests(TestCase):
    def test_save_and_load(self):
        time = timezone.now() + datetime.timedelta(days=30)


from django.test import TestCase
from models import *


class LineModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Line.objects.create(
            device_type='Block',
            device_name='NG123',

        )

    def setUp(self) -> None:
        pass

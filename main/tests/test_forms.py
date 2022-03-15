from http import HTTPStatus
from pprint import pprint

from django.test import TestCase

from main.forms import AddPostForm, AddEquipmentForm
from main.models import Category, Line, TestType, User, Equipment, Mode


class PostFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Line.objects.create(
            device_type='TestBlock',
            device_name='TestNG',
            quantity=321,
            number='number5',
            date_start="2022-01-31",
            date_stop_expected="2022-02-28",
            test_type=TestType.objects.create(name='Периодические'),
            executor=User.objects.create(username='User'),
            cats=Category.objects.create(name='Текущие')
        )
        User.objects.create(
            username='TestUser1'
        )
        Category.objects.create(
            name='Завершенные'
        )

    def test_add_eq_work(self):
        form = AddEquipmentForm(data={
            'line_id': Line.objects.get(pk=1),
            'eq_name': Equipment.objects.create(name='TestEq'),
            'date_start': '2021-05-01',
            'date_stop': '2021-07-01',
            'work_time': 1,
            'executor': User.objects.get(username='TestUser1'),
            'mode': Mode.objects.create(name='TestMode')
        })
        self.assertEquals(form.errors, {})

    def test_add_eq_work_time_error(self):
        """
        Test for checking impossibility add EquipmentWork with more,
        then 720 hours of work time per month
        """
        form = AddEquipmentForm(data={
            'line_id': Line.objects.get(pk=1),
            'eq_name': Equipment.objects.create(name='TestEq'),
            'date_start': '2021-05-01',
            'date_stop': '2021-07-01',
            'work_time': 900,
            'executor': User.objects.get(username='TestUser1'),
            'mode': Mode.objects.create(name='TestMode')
        })
        # Error by max limit of monthly work time
        self.assertEquals(str(type(form.errors)), "<class 'django.forms.utils.ErrorDict'>")

    def test_add_post_form_in_progress(self):
        form = AddPostForm(data={
            'device_type': 'TestType',
            'device_name': 'TestName',
            'number': 'Mamba#5',
            'quantity': 100,
            'date_start': '2021-07-01',
            'date_stop': '2021-07-01',
            'date_stop_expected': '2021-07-01',
            'test_type': TestType.objects.get(pk=1),
            'executor': User.objects.get(pk=1),
            'cats': Category.objects.get(pk=1)
        })
        self.assertEquals(form.errors, {})

    def test_add_post_form_complete(self):
        """
        Test for check impossibility of setting Category.pk=2,
        if not all fields are fill.
        """
        form = AddPostForm(data={
            'device_type': 'TestType1',
            'device_name': 'TestName1',
            'number': 'Mamba#3',
            'quantity': 1000,
            'date_start': '2021-07-01',
            'date_stop': '2021-07-01',
            'date_stop_expected': '2021-07-01',
            'test_type': TestType.objects.get(pk=1),
            'executor': User.objects.get(pk=1),
            'cats': Category.objects.get(pk=2)
        })
        self.assertEquals(str(type(form.errors)), "<class 'django.forms.utils.ErrorDict'>")

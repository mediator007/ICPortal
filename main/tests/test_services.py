from django.contrib.auth.models import User
from django.test import TestCase

from main.models import Line, Category, TestType, Equipment, EquipmentWork, Mode
from main.views_services import *


class LineModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Line.objects.create(
            device_type='TestBlock',
            device_name='TestNG',
            dec_number='TestNG',
            quantity=321,
            date_start="2022-01-31",
            date_stop_expected="2022-02-28",
            test_type=TestType.objects.create(name='Periodic'),
            executor=User.objects.create(username='User'),
            cats=Category.objects.create(name='On')
        )
        Line.objects.create(
            device_type='TestBlock1',
            device_name='TestNG1',
            quantity=341,
            date_start="2022-01-01",
            date_stop_expected="2020-01-29",
            date_stop="2022-01-29",
            test_type=TestType.objects.create(name='Type'),
            executor=User.objects.create(username='User1'),
            cats=Category.objects.create(name='Off')
        )
        Equipment.objects.create(
            name='01. equipment',
            number='3232',
            order_number=999
        )
        EquipmentWork.objects.create(
            line_id=Line.objects.get(device_name="TestNG"),
            eq_name=Equipment.objects.get(name="01. equipment"),
            mode = Mode.objects.create(name='MODE'),
            date_start="2021-01-31",
            date_stop="2021-02-28",
            work_time=700,
            executor=User.objects.get(username='User')
        )
        EquipmentWork.objects.create(
            line_id=Line.objects.get(device_name="TestNG"),
            eq_name=Equipment.objects.get(name="01. equipment"),
            mode=Mode.objects.create(name='MODE'),
            date_start="2021-01-31",
            date_stop="2021-02-28",
            work_time= 2,
            executor=User.objects.get(username='User')
        )

    def test_list_of_complete_dates(self):
        check = list_of_complete_dates()
        true_list = ['2022-03', '2022-02', '2022-01']
        self.assertEquals(check, true_list)

    def test_list_of_month_complete_lines(self):
        check = list_of_month_complete_lines('2022-01')
        check = str(check)
        true_list = '<QuerySet [<Line: TestNG1>]>'
        self.assertEquals(check, true_list)

    def test_get_year_month(self):
        check = get_year_month('1969-06')
        true_dict = {'year': '1969', 'month': '06'}
        self.assertEquals(check, true_dict)

    def test_get_month_sum_eq_work(self):
        check = get_month_sum_eq_work(1, '2021-02')
        true_sum = 702
        self.assertEquals(check, true_sum)

    def test_get_act_number(self):
        check = get_act_number()
        current_month = datetime.date.today()
        month = current_month.strftime("%m")
        true_act = f'01/{month}'
        self.assertEquals(check, true_act)

    def test_get_search_results(self):
        q = Line.objects.get(pk=1).device_name
        check = get_search_results(q)
        true_result = Line.objects.get(pk=1)
        self.assertEquals(check[0], true_result)




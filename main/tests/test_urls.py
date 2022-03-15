from django.contrib.auth.models import User
from django.test import TestCase

from main.models import Line, Category, TestType, Equipment, EquipmentWork, Mode


class LineModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Line.objects.create(
            device_type='TestBlock',
            device_name='TestNG',
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
            date_start="2020-02-01",
            date_stop_expected="2020-03-29",
            date_stop="2021-03-29",
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

    def test_url_home(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_url_addpage(self):
        response = self.client.post('/addpage/', follow=True)
        self.assertEquals(response.status_code, 200)

    def test_url_add_equipment_work(self):
        response = self.client.post(f'/addEquipmentWork/{Line.objects.get(device_name="TestNG").pk}/', follow=True)
        self.assertEquals(response.status_code, 200)

    def test_url_edit_equipment_work(self):
        response = self.client.post(f'/editEquipmentWork/'
                                    f'{Line.objects.get(device_name="TestNG").pk}/'
                                    f'{EquipmentWork.objects.get(date_stop="2021-02-28").pk}/',
                                    follow=True)
        self.assertEquals(response.status_code, 200)

    def test_url_post(self):
        response = self.client.get(f'/post/{Line.objects.get(device_name="TestNG").pk}/')
        self.assertEquals(response.status_code, 200)

    def test_url_editline(self):
        response = self.client.post(f'/editLine/{Line.objects.get(device_name="TestNG").pk}/', follow=True)
        self.assertEquals(response.status_code, 200)

    def test_url_reports(self):
        response = self.client.get('/reports/')
        self.assertEquals(response.status_code, 200)

    def test_url_reports_eq(self):
        response = self.client.get(f'/reports/{Equipment.objects.get(name="01. equipment").pk}/')
        self.assertEquals(response.status_code, 200)

    def test_url_reports_date(self):
        response = self.client.get(f'/reports/1/2022-03')
        self.assertEquals(response.status_code, 200)

    def test_url_complete(self):
        response = self.client.get('/complete/')
        self.assertEquals(response.status_code, 200)

    def test_url_complete_date(self):
        response = self.client.get(f'/complete/2021-03')
        self.assertEquals(response.status_code, 200)

    def test_url_search_results(self):
        response = self.client.get('/search_results/?q=TestNG')
        self.assertEquals(response.status_code, 200)

    def test_url_getactcnumber(self):
        response = self.client.get(f'/getactnumber/{Line.objects.get(device_name="TestNG").pk}/')
        self.assertEquals(response.status_code, 200)



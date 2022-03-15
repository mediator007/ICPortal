from django.test import TestCase

from contract.models import *
from main.models import Equipment, EquipmentWork, Mode


class LineContractModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        LineContract.objects.create(
            organization=Organization.objects.create(name='TestGOZ'),
            device="TestGozDev",
            enter_number='ew/ew123',
            request_date='2020-01-01',
            executor=User.objects.create(username='User1'),
            status=Category.objects.create(name='On'),
            full_status=Category.objects.get(name='On')
        )
        LineContract.objects.create(
            organization=Organization.objects.create(name='TestRIRV'),
            device="TestRirvDev",
            enter_number='ew/e2eddsacvv23',
            request_date='2021-07-01',
            executor=User.objects.create(username='User2'),
            status=Category.objects.create(name='Off'),
            full_status=Category.objects.get(name='Off')
        )

        EquipmentWork.objects.create(
            line_contract=LineContract.objects.get(device="TestGozDev"),
            eq_name=Equipment.objects.create(name="01. equipment"),
            mode=Mode.objects.create(name='MODE'),
            date_start="2020-01-31",
            date_stop="2020-02-2",
            work_time=700,
            executor=User.objects.get(username='User1')
        )

    def test_url_home(self):
        response = self.client.get('/contract/', follow=True)
        self.assertEquals(response.status_code, 200)

    def test_url_addpage(self):
        response = self.client.post('/contract/addpage/', follow=True)
        self.assertEquals(response.status_code, 200)

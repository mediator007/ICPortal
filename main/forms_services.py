from django.core.exceptions import ValidationError
from main.models import Category, TestType


def check_addpostform(
        status, test_type, date_stop,
        customer, act_number, act, programm
):
    if status == Category.objects.get(pk=2) and test_type == \
            TestType.objects.get(name='Периодические'):

        if (
                date_stop is None or
                customer is None or
                act is None or
                programm is None or
                act_number is None
        ):
            raise ValidationError(
                "Нельзя установить статус 'Завершенные' без заполнения всех полей"
            )


def check_monthly_equip_work_time(
        date_input, eq_name,
        work_time, equip
):
    time_sum = 0
    for eq in equip:
        if eq.date_stop.strftime("%Y-%m") == date_input.strftime("%Y-%m"):
            time_sum += eq.work_time
    if (work_time + time_sum) > 700:
        raise ValidationError(
            f"Наработка камеры заполнена, выберите другую камеру. Ограничение месячной наработки \
                    700 часов. ИО № {eq_name} - наработка {time_sum} часов."
        )
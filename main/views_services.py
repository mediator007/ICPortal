import datetime

from dateutil.relativedelta import relativedelta
from django.db.models import Min
from django.http import request

from main.models import Line, Category, EquipmentWork


def list_of_complete_dates():
    """
    Create list of dates from the oldest Line object
    date_stop in db for today s date month by month
    """
    date_list = []
    current_date = datetime.date.today()
    oldest_date = Line.objects.all().aggregate(Min('date_stop'))
    while current_date.strftime("%Y-%m") != oldest_date['date_stop__min'].strftime("%Y-%m"):
        date_list.append(oldest_date['date_stop__min'].strftime("%Y-%m"))
        oldest_date['date_stop__min'] = oldest_date['date_stop__min'] + relativedelta(months=1)
    date_list.append(current_date.strftime("%Y-%m"))
    date_list.sort(reverse=True)
    return date_list


def list_of_month_complete_lines(date):
    """
    Create list of Lines objects, which
    date_stop month == date
    """
    year = date[:4]
    month = date[-2:]
    complete_cat = Category.objects.get(id=2)
    line_list = Line.objects.filter(date_stop__year=year,
                                    date_stop__month=month,
                                    cats=complete_cat)
    return line_list


def list_of_dates_for_equip(eq_pk: int):
    """
    Create list of dates from oldest EquipmentWork object
    date_stop for today month by month
    """
    date_list = []
    current_date = datetime.date.today()
    oldest_date = EquipmentWork.objects.filter(eq_name_id=eq_pk).aggregate(Min('date_stop'))
    while current_date.strftime("%Y-%m") != oldest_date['date_stop__min'].strftime("%Y-%m"):
        date_list.append(oldest_date['date_stop__min'].strftime("%Y-%m"))
        oldest_date['date_stop__min'] = oldest_date['date_stop__min'] + relativedelta(months=1)
    date_list.append(current_date.strftime("%Y-%m"))
    date_list.sort(reverse=True)
    return date_list


def get_year_month(date: str):
    """
    Separate month and year from date string
    """
    year = date[:4]
    month = date[-2:]
    return {'year': year, 'month': month}


def get_month_sum_eq_work(eq_pk, date):
    """ Get sum of hours equipment work in this month """
    equipment_work = EquipmentWork.objects.filter(eq_name=eq_pk)
    hour_sum = 0
    for eq in equipment_work:
        if eq.date_stop.strftime("%Y-%m") == date:
            hour_sum += eq.work_time
    return hour_sum


def get_act_number() -> str:
    """
    Create new act_number
    """
    # Get current date
    current_month = datetime.date.today()
    year = current_month.strftime("%Y")
    month = current_month.strftime("%m")
    # Sort act numbers on this year and month
    current_act_number = Line.objects.filter(date_stop__year=year,
                                             date_stop__month=month).order_by('-act_number')
    # Take last act number, if not exist, take 00/00
    try:
        current_number = current_act_number[0].act_number
    except Exception as e:
        print(f'No act number in this month yet. Error:{e}')
        current_number = '00/00'
    # Add 1 to last two digits in act number
    current_number = current_number[:2]
    current_number = int(current_number) + 1
    if current_number in range(9):
        act_number = f"0{current_number}/{month}"
    else:
        act_number = f"{current_number}/{month}"
    return act_number


# Need to integrate to 'search' func in view.py
# for unification context
def get_search_results(q: str):
    results_name = Line.objects.filter(device_name=q)
    results_dec = Line.objects.filter(dec_number=q)
    # | for sum two query sets with unique values
    res = results_name | results_dec
    print(res)
    return res

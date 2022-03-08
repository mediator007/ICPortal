from django.db.models import Count
from dateutil.relativedelta import relativedelta
import datetime

from .models import *

menu = [
        {'title': "Главная", 'url_name': 'home'},
        {'title': "Договорные испытания", 'url_name': 'contract'},
        {'title': "Наработка", 'url_name': 'reports'}
]

class DataMixin:
    paginate_by = 8

    def get_user_context(self, **kwargs):
        context = kwargs
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(0)
        context['menu'] = user_menu
        return context


def last_act():
    current_date = datetime.date.today()
    year = current_date.strftime("%Y")
    month = current_date.strftime("%m")
    devices = Line.objects.filter(date_stop__year=year, date_stop__month=month)
    for item in devices:
        print(item)
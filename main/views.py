import operator
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.db.models import Min
from dateutil.relativedelta import relativedelta
import datetime
# Type annotations
from typing import List, Any, Union
#from Tools.scripts.make_ctype import method

from .forms import *
from .models import *
from .utils import DataMixin


class LineHome(DataMixin, ListView):
    model = Line
    template_name = 'main/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Line.objects.filter(cats=1)


@login_required
def add_page(request):
    title = 'Добавить запись'
    # form = AddPostForm()
    type_list = TestType.objects.all()
    status_list = Category.objects.all()
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(f'/')

    context = {'type_list': type_list, 'status_list': status_list, 'title': title}
    return render(request, "main/addpage.html", context)


def pageNotFound(request: Any,
                 exception: Any) -> HttpResponseNotFound:
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class ShowPost(DataMixin, DetailView):
    model = Line
    template_name = 'main/post.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['equipment'] = EquipmentWork.objects.all()
        print(context)
        return context


@login_required
def add_equipment_work(request,
                       id: int) -> Union[HttpResponseNotFound, HttpResponseRedirect]:
    form = AddEquipmentForm()
    eq_list = Equipment.objects.all()
    if request.method == 'POST':
        form = AddEquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseNotFound('<h1>Наработка не привязана к испытаниям</h1>')
        return redirect(f'/')

    context = {'form': form, 'eq_list': eq_list, 'pk': id}
    return render(request, "main/addequipment.html", context)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'

    # context_object_name = 'active_user'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def editLine(request,
                       id: int) -> Union[HttpResponseNotFound, HttpResponseRedirect]:
    post = Line.objects.get(id=id)
    form = AddPostForm(instance=post)
    act_number = post.act_number
    if post.cats == Category.objects.get(id=1):
        if request.method == 'POST':
            form = AddPostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                return redirect('/')
        context = {'form': form, 'post': post, 'act_number': act_number}
        return render(request, "main/editLine.html", context)
    else:
        return HttpResponseNotFound('<h1>Запрет изменения Завершенных испытаний</h1>')


@login_required
def add_equipment_work(request,
                       id: int) -> Union[HttpResponseNotFound, HttpResponseRedirect]:
    form = AddEquipmentForm()
    if request.method == 'POST':
        form = AddEquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form, 'id': id}
    return render(request, "main/addequipment.html", context)


@login_required
def editEquipmentWork(request, id, id1):
    post = EquipmentWork.objects.get(id=id1)
    form = AddEquipmentForm(instance=post)
    eq_list = Equipment.objects.all()
    line = Line.objects.get(id=id)
    print(line.executor)

    if request.method == 'POST':
        form = AddEquipmentForm(request.POST, instance=post)  # instance = post для автозаполнения записи
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form, 'eq_list': eq_list, 'id': id, 'line': line}
    return render(request, "main/editEquipmentWork.html", context)


def search(request):
    q = request.GET.get('q')
    results_name = Line.objects.filter(device_name=q)
    results_dec = Line.objects.filter(dec_number=q)
    context = {'results_name': results_name, 'results_dec': results_dec, 'q': q}
    return render(request, 'main/search_results.html', context)


def complete(request):
    try:
        list = []
        current_date = datetime.date.today()
        oldest_date = Line.objects.all().aggregate(Min('date_stop'))
        while current_date.strftime("%Y-%m") != oldest_date['date_stop__min'].strftime("%Y-%m"):
            list.append(oldest_date['date_stop__min'].strftime("%Y-%m"))
            oldest_date['date_stop__min'] = oldest_date['date_stop__min'] + relativedelta(months=1)
        list.append(current_date.strftime("%Y-%m"))
        list.sort(reverse=True)
        context = {'list': list}
        return render(request, 'main/complete_org.html', context)
    except:
        return HttpResponseNotFound('<h1>Нет завершенных изделий</h1>')


def complete_date(request, date):
    try:
        year = date[:4]
        month = date[-2:]
        complete = Category.objects.get(id=2)
        list = Line.objects.filter(date_stop__year=year, date_stop__month=month, cats=complete)
        context = {'list': list, 'date': date}
        return render(request, 'main/complete_date.html', context)
    except:
        return HttpResponseNotFound('<h1>Нет завершенных изделий</h1>')


# List of equipment
def reports(request):
    equipment = Equipment.objects.order_by('name')
    context = {'equipment': equipment}
    return render(request, 'main/reports.html', context)


# List of months for chosen equipment
def reports_eq(request, id):
    try:
        list = []
        current_date = datetime.date.today()
        oldest_date = EquipmentWork.objects.filter(eq_name_id=id).aggregate(Min('date_stop'))
        while current_date.strftime("%Y-%m") != oldest_date['date_stop__min'].strftime("%Y-%m"):
            list.append(oldest_date['date_stop__min'].strftime("%Y-%m"))
            oldest_date['date_stop__min'] = oldest_date['date_stop__min'] + relativedelta(months=1)
        list.append(current_date.strftime("%Y-%m"))
        list.sort(reverse=True)
        eq = Equipment.objects.get(id=id)
        context = {'list': list, 'eq': eq}
        return render(request, 'main/reportsEq.html', context)
    except:
        return HttpResponseNotFound('<h1>Нет наработки</h1>')


# Equipment work in this month
def report_date(request, id, date):
    year = date[:4]
    month = date[-2:]
    # month work sum
    sum = 0
    equipment_work = EquipmentWork.objects.filter(eq_name=id)
    for eq in equipment_work:
        if eq.date_stop.strftime("%Y-%m") == date:
            sum += eq.work_time
    equipment = Equipment.objects.get(id=id)
    # context for label
    device = Line.objects.all()
    list = EquipmentWork.objects.filter(date_stop__year=year, date_stop__month=month, eq_name=equipment)
    context = {'equipment': equipment, 'date': date, 'sum': sum, 'device': device, 'list': list}
    return render(request, 'main/report_date.html', context)


def get_act_number(request, id):
    current_month = datetime.date.today()
    year = current_month.strftime("%Y")
    month = current_month.strftime("%m")
    # Last act number
    current_act_number = Line.objects.filter(date_stop__year=year, date_stop__month=month).order_by('-act_number')
    try:
        current_number = current_act_number[0].act_number
    # If mo act number in this month
    except:
        current_number = '00/00'
    current_number = current_number[:2]
    current_number = int(current_number) + 1
    if current_number in range(9):
        act_number = f"0{current_number}/{month}"
    else:
        act_number = f"{current_number}/{month}"
    # Write act number to db
    Line.objects.filter(id=id).update(act_number=act_number)
    device = Line.objects.get(id=id)
    context = {'act_number': act_number, 'device': device}
    return render(request, "main/getactnumber.html", context)

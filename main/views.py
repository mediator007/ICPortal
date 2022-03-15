from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from typing import List, Any, Union

from main.forms import *
from main.models import *
from main.utils import DataMixin, menu
from main.views_services import *


class LineHome(DataMixin, ListView):
    """
    Create context from Line objects with cats=1 in home page
    """
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
    """
    Create page with form to add new Line object
    """
    title = 'Добавить запись'
    type_list = TestType.objects.all()
    status_list = Category.objects.all()
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(f'/')
    context_menu = menu
    context = {
        'type_list': type_list, 'status_list': status_list,
        'title': title, 'menu': context_menu
    }
    return render(request, "main/addpage.html", context)


def pageNotFound(request, exception) -> HttpResponseNotFound:
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


class ShowPost(DataMixin, DetailView):
    """
    Create page with all fields of Line object and all
    EquipmentWork objects which belong to this Line object
    """
    model = Line
    template_name = 'main/post.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['equipment'] = EquipmentWork.objects.all()
        context['menu'] = menu
        return context


@login_required
def add_equipment_work(request,
                       id: int) -> Union[HttpResponseNotFound, HttpResponseRedirect]:
    """
    Create new Equipment work object which will belong
    Line object with pk=id
    """
    form = AddEquipmentForm()
    eq_list = Equipment.objects.all()
    if request.method == 'POST':
        form = AddEquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f'/post/{id}/')
    context_menu = menu
    context = {'form': form, 'eq_list': eq_list, 'pk': id, 'menu': context_menu}
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
    """
    Make page with form to edit Line object with pk=id
    """
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
        context_menu = menu
        context = {'error': 'Запрет изменения Завершенных испытаний', 'menu': context_menu}
        return render(request, 'main/error.html', context)


@login_required
def add_equipment_work(request,
                       id: int) -> Union[HttpResponseNotFound, HttpResponseRedirect]:
    form = AddEquipmentForm()
    if request.method == 'POST':
        form = AddEquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context_menu = menu
    context = {'form': form, 'id': id, 'menu': context_menu}
    return render(request, "main/addequipment.html", context)


@login_required
def editEquipmentWork(request, id, id1):
    """
    Get view for form to edit EquipmentWork object pk=id1
    which belongs Line object pk=id
    """
    post = EquipmentWork.objects.get(id=id1)
    form = AddEquipmentForm(instance=post)
    eq_list = Equipment.objects.all()
    line = Line.objects.get(id=id)
    print(line.executor)

    if request.method == 'POST':
        # Auto insert data in form
        form = AddEquipmentForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('/')
    context_menu = menu
    context = {
        'form': form, 'eq_list': eq_list,
        'id': id, 'line': line, 'menu': context_menu
    }
    return render(request, "main/editEquipmentWork.html", context)


def search(request):
    """
    Get context with results of searching
    """
    q = request.GET.get('q')
    results_name = Line.objects.filter(device_name=q)
    results_dec = Line.objects.filter(dec_number=q)
    context_menu = menu
    context = {'results_name': results_name, 'results_dec': results_dec,
               'q': q, 'menu': context_menu
               }
    return render(request, 'main/search_results.html', context)


def complete(request):
    """
    Create context with a list of dates from the oldest
    Line.date_stop in db for today s date month by month
    """
    try:
        date_list = list_of_complete_dates()
        context_menu = menu
        context = {'list': date_list, 'menu': context_menu}
        return render(request, 'main/complete.html', context)
    except Exception as e:
        print(f'No complete dates. Error: {e}')
        context_menu = menu
        context = {'error': 'Нет завершенных изделий', 'menu': context_menu}
        return render(request, 'main/error.html', context)


def complete_date(request, date: str):
    """
    Create a context with a list of Lines objects, which
    date_stop month == date
    """
    try:
        line_list = list_of_month_complete_lines(date)
        context_menu = menu
        context = {'list': line_list, 'date': date, 'menu': context_menu}
        return render(request, 'main/complete_date.html', context)
    except Exception as e:
        print(f'No complete Line objects. Error: {e}')
        context_menu = menu
        context = {'error': 'Нет завершенных изделий', 'menu': context_menu}
        return render(request, 'main/error.html', context)


def reports(request):
    """ Create context with list of equipment """
    equipment = Equipment.objects.order_by('order_number')
    context_menu = menu
    context = {'equipment': equipment, 'menu': context_menu}
    return render(request, 'main/reports.html', context)


def reports_eq(request, eq_pk: int):
    """
    Create a context with list of dates from oldest EquipmentWork
    object for today month by month
    """
    try:
        date_list = list_of_dates_for_equip(eq_pk)
        eq = Equipment.objects.get(id=eq_pk)
        context_menu = menu
        context = {'list': date_list, 'eq': eq, 'menu': context_menu}
        return render(request, 'main/reportsEq.html', context)
    except Exception as e:
        print(f'No Equipment work objects. Error: {e}')
        context_menu = menu
        context = {'error': 'Нет наработки', 'menu': context_menu}
        return render(request, 'main/error.html', context)


def report_date(request, eq_pk: int, date: str):
    """
    Make context with EquipmentWork objects which belong Equipment object
    with pk=eq_pk and month from 'date'
    """
    year = get_year_month(date)['year']
    month = get_year_month(date)['month']
    hour_sum = get_month_sum_eq_work(eq_pk, date)
    equipment = Equipment.objects.get(id=eq_pk)
    # Need to edit for increase speed. Make filter for Line.date_stop > date
    device = Line.objects.all()
    eq_work_list = EquipmentWork.objects.filter(date_stop__year=year, date_stop__month=month, eq_name=equipment)
    context_menu = menu
    context = {
        'equipment': equipment, 'date': date,
        'sum': hour_sum, 'device': device,
        'list': eq_work_list, 'menu': context_menu
    }
    return render(request, 'main/report_date.html', context)


def get_act_context(request, post_id):
    act_number = get_act_number()
    # Write act number to db
    Line.objects.filter(id=post_id).update(act_number=act_number)
    device = Line.objects.get(id=post_id)
    context_menu = menu
    context = {'act_number': act_number, 'device': device, 'menu': context_menu}
    return render(request, "main/getactnumber.html", context)

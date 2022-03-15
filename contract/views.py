from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from main.models import EquipmentWork
from main.utils import DataMixin, menu
from contract.forms import *


class LineContractHome(LoginRequiredMixin, PermissionRequiredMixin, DataMixin, ListView):
    """
    Create context for 'home' page with LineContract
    objects that have full_status=1 'in progress'
    """
    # 'contract' - app name, 'linecontract' - model name
    permission_required = 'contract.view_linecontract'
    # Was edit mixins.py class AccessMixin in
    # raise_exception to redirect to login page
    raise_exception = False
    model = LineContract
    template_name = 'contract/index_contract.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Текущие договорные")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return LineContract.objects.filter(full_status=1)


class CompleteOrganizations(LoginRequiredMixin, PermissionRequiredMixin, DataMixin, ListView):
    """
    Create context with list of existing
    organizations from Organization class
    """
    permission_required = 'contract.view_linecontract'
    template_name = 'contract/complete_org.html'
    context_object_name = 'organizations'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Организации")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Organization.objects.all()


class Complete(LoginRequiredMixin, PermissionRequiredMixin, DataMixin, ListView):
    """
    Create context for 'complete' page with LineContract
    objects that have full_status=2 'completed' and chosen organization
    'org' in queryset
    """
    permission_required = 'contract.view_linecontract'
    raise_exception = False
    template_name = 'contract/complete.html'
    context_object_name = 'complete'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Завершенные")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        org = self.kwargs.get('org', None)
        if org is not None:
            return LineContract.objects.filter(organization_id=org, full_status=2)


class ShowPost(LoginRequiredMixin, PermissionRequiredMixin, DataMixin, DetailView):
    """
    Create context for page with LineContract object card, and also
    EquipmentWork and Letters objects which belongs to LineContract
    object pk=post_id
    """
    permission_required = 'contract.view_linecontract'
    raise_exception = False
    model = LineContract
    template_name = 'contract/post.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['equipment'] = EquipmentWork.objects.all()
        context['letters'] = Letters.objects.all()
        c_def = self.get_user_context(title="Карточка испытания")
        return dict(list(context.items()) + list(c_def.items()))


@login_required
@permission_required('contract.add_linecontract', raise_exception=False)
def add_page(request):
    """
    Create page with form to add new LineContract object
    """
    title = 'Добавить запись'
    form = AddPostForm1()
    if request.method == 'POST':
        form = AddPostForm1(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f'/')
    context_menu = menu
    context = {'title': title, 'form': form, 'menu': context_menu}
    return render(request, "contract/addpage.html", context)


@login_required
@permission_required('contract.add_linecontract', raise_exception=False)
# n - number of AddPostForm
def edit_line(request, id: int, n: int):
    """
    Create page with one of AddPostForm_'n'_, that wil edit fields
    of LineContract object pk=id from 'n' block
    """
    post = LineContract.objects.get(id=id)
    # Using different Form classes
    str_class = f'AddPostForm{n}'
    # Remove str to class name from forms.py
    form = eval(str_class)(instance=post)
    if post.full_status == Category.objects.get(id=1):
        if request.method == 'POST':
            form = eval(str_class)(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                return redirect('/')
        context_menu = menu
        context = {'form': form, 'post': post, 'menu': context_menu}
        return render(request, "contract/editline.html", context)
    else:
        return HttpResponseNotFound('<h1>Запрет изменения Завершенных испытаний</h1>')


@login_required
@permission_required('contract.add_linecontract', raise_exception=False)
def search(request):
    """
    Create context with searching results
    """
    q = request.GET.get('q')
    results_device = LineContract.objects.filter(device=q)
    try:
        organization = Organization.objects.get(name=q)
        results_organization = LineContract.objects.filter(organization=organization.pk)
        context = {'res1': results_device, 'res2': results_organization, 'q': q}
    except Exception as e:
        print(e)
        context = {'res1': results_device, 'q': q}
    finally:
        return render(request, 'contract/search.html', context)


@login_required
@permission_required('contract.add_linecontract', raise_exception=False)
def add_letter(request, num):
    """
    Create page with form for adding Letter object
    """
    title = 'Добавить письмо'
    form = LetterPostForm()
    if request.method == 'POST':
        form = LetterPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f'/')

    context = {'title': title, 'form': form, 'num': num}
    return render(request, "contract/addletter.html", context)


@login_required
@permission_required('contract.add_linecontract', raise_exception=False)
def edit_letter(request, num, num1):
    """
    Create page with form to edit Letter object pk=num1 that belong
    to LineContract object pk=num
    """
    post = Letters.objects.get(id=num1)
    form = LetterPostForm(instance=post)
    if request.method == 'POST':
        # instance use for autofilling form
        form = LetterPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form, 'id': num}
    return render(request, "contract/editletter.html", context)


@login_required
@permission_required('contract.add_linecontract', raise_exception=False)
def add_equipment_work(request, num: int):
    """
    Create a page with form to add Equipment work object
    that will belong to LineContract object pk=num
    """
    form = AddEquipmentForm()
    if request.method == 'POST':
        form = AddEquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form, 'id': num}
    return render(request, "contract/addequipment.html", context)


@login_required
@permission_required('contract.add_linecontract', raise_exception=False)
def edit_equipment_work(request, num: int, num1: int):
    """
    Create page with form to edit EquipmentWork object pk=num1,
    that belong LineContract object pk=num
    """
    post = EquipmentWork.objects.get(id=num1)
    form = AddEquipmentForm(instance=post)
    if request.method == 'POST':
        form = AddEquipmentForm(request.POST, instance=post)  # instance = post для автозаполнения записи
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form, 'id': num}
    return render(request, "contract/editEquipmentWork.html", context)
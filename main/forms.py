# from asyncio.windows_events import NULL
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError

from main.models import *
from main.forms_services import *


class AddPostForm(forms.ModelForm):
    """
    Form to add new Line object
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Line
        fields = '__all__'
        widgets = {
            'date_start': forms.SelectDateWidget(),
            'date_stop_expected': forms.SelectDateWidget(),
            'date_stop': forms.SelectDateWidget(),
            'comment': forms.Textarea()
        }

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('cats')
        test_type = cleaned_data.get('test_type')
        date_stop = cleaned_data.get('date_stop')
        act_number = cleaned_data.get('act_number')
        customer = cleaned_data.get('customer')
        act = cleaned_data.get('act')
        programm = cleaned_data.get('programm')
        # Checking all fields before change status in periodic tests
        check_addpostform(
            status, test_type, date_stop,
            customer, act_number, act, programm
        )


class AddEquipmentForm(forms.ModelForm):
    """
    Form to add EquipmentWork object.
    Line_id field filling automatically.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['eq_name'].empty_label = "Оборудование не выбрано"
        self.fields['mode'].empty_label = "Режим не выбран"

    class Meta:
        model = EquipmentWork
        fields = [
            'eq_name', 'mode', 'date_start',
            'date_stop', 'work_time',
            'executor', 'line_id',
        ]
        widgets = {
            'date_stop': forms.SelectDateWidget(),
            'date_start': forms.SelectDateWidget()
        }


    def clean(self):
        cleaned_data = super().clean()
        name_input = cleaned_data.get('eq_name')
        date_input = cleaned_data.get('date_stop')
        eq_name = Equipment.objects.get(name=name_input)
        work_time = cleaned_data.get('work_time')
        equip = EquipmentWork.objects.filter(eq_name=eq_name)
        # Checking max monthly working time fo equipment
        check_monthly_equip_work_time(
                date_input, eq_name,
                work_time, equip
        )


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

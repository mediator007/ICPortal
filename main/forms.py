# from asyncio.windows_events import NULL
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import *


class AddPostForm(forms.ModelForm):  # , User):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['cats'].empty_label = "Категория не выбрана"
        # self.fields['executor'] = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Line
        fields = '__all__'
        # widgets = {'executor': forms.HiddenInput()}

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
        if status == Category.objects.get(name='Завершенные') and test_type == TestType.objects.get(
                name='Периодические'):
            if (date_stop == None or customer == None or act == None or programm == None):  # or act_number == None
                raise ValidationError(
                    "Нельзя установить статус 'Завершенные' без заполнения остальных полей"
                )


class AddEquipmentForm(forms.ModelForm):
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

    # Checking max monthly working time fo equipment
    def clean(self):
        cleaned_data = super().clean()
        name_input = cleaned_data.get('eq_name')
        date_input = cleaned_data.get('date_stop')
        eq_name = Equipment.objects.get(name=name_input)
        work_time = cleaned_data.get('work_time')
        equip = EquipmentWork.objects.filter(eq_name=eq_name)
        sum = 0
        for eq in equip:
            if eq.date_stop.strftime("%Y-%m") == date_input.strftime("%Y-%m"):
                sum += eq.work_time
        if (work_time + sum) > 700:
            raise ValidationError(
                f"Наработка камеры заполнена, выберите другую камеру. Ограничение месячной наработки \
                700 часов. ИО № {eq_name} - наработка {sum} часов."
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

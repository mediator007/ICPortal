from django import forms
from django.core.exceptions import ValidationError

from .models import *
from main.models import EquipmentWork, Equipment


class AddPostForm1(forms.ModelForm):
    class Meta:
        model = LineContract
        fields = [
            'organization', 'device',
            'enter_number', 'request_date',
            'status', 'full_status', 'executor'
        ]
        widgets = {
            'request_date': forms.SelectDateWidget()
        }


class AddPostForm2(forms.ModelForm):
    class Meta:
        model = LineContract
        fields = [
            'customer_out_number', 'customer_out_date',
            'customer_phone'
        ]
        widgets = {
            'customer_out_date': forms.SelectDateWidget()
        }


class AddPostForm3(forms.ModelForm):
    class Meta:
        model = LineContract
        fields = [
            'official_memo', 'official_memo_date'
        ]
        widgets = {
            'official_memo_date': forms.SelectDateWidget()
        }


class AddPostForm4(forms.ModelForm):
    class Meta:
        model = LineContract
        fields = [
            'personal_time', 'personal_time_spz',
            'personal_time_vp'
        ]


class AddPostForm5(forms.ModelForm):
    class Meta:
        model = LineContract
        fields = [
            'expected_test_date'
        ]
        widgets = {
            'expected_test_date': forms.SelectDateWidget()
        }


class AddPostForm6(forms.ModelForm):
    class Meta:
        model = LineContract
        fields = [
            'notification_date', 'notification_name'
        ]
        widgets = {
            'notification_date': forms.SelectDateWidget()
        }


class AddPostForm7(forms.ModelForm):
    class Meta:
        model = LineContract
        fields = [
            'status', 'comment'
        ]


class AddPostForm8(forms.ModelForm):
    class Meta:
        model = LineContract
        fields = [
            'expected_cost', 'fact_cost'
        ]


class AddPostForm9(forms.ModelForm):
    class Meta:
        model = LineContract
        fields = [
            'bill', 'bill_date',
            'bill_date_signing', 'bill_date_final',
            'in_gov_contract_from'
        ]
        widgets = {
            'bill_date': forms.SelectDateWidget(),
            'bill_date_signing': forms.SelectDateWidget(),
            'bill_date_final': forms.SelectDateWidget()
        }


class AddPostForm10(forms.ModelForm):
    class Meta:
        model = LineContract
        fields = [
            'price_protocol', 'RKM_request',
            'deal_number', 'price_letter_number',
            'out_letter_number', 'send_date'
        ]
        widgets = {
            'send_date': forms.SelectDateWidget()
        }


class AddPostForm11(forms.ModelForm):
    class Meta:
        model = LineContract
        fields = [
            'bill_number', 'pay_bill_date'
        ]
        widgets = {
            'pay_bill_date': forms.SelectDateWidget()
        }


class AddPostForm12(forms.ModelForm):
    class Meta:
        model = LineContract
        fields = [
            'pp_number', 'pp_date'
        ]
        widgets = {
            'pp_date': forms.SelectDateWidget()
        }


class AddPostForm13(forms.ModelForm):
    class Meta:
        model = LineContract
        fields = [
            'service_act_number', 'service_act_date'
        ]
        widgets = {
            'service_act_date': forms.SelectDateWidget()
        }


class AddPostForm14(forms.ModelForm):
    class Meta:
        model = LineContract
        fields = [
            'bill_facture', 'bill_facture_date'
        ]
        widgets = {
            'bill_facture_date': forms.SelectDateWidget()
        }


class AddPostForm15(forms.ModelForm):
    class Meta:
        model = LineContract
        fields = [
            'spz', 'spz_date'
        ]
        widgets = {
            'spz_date': forms.SelectDateWidget()
        }


class AddPostForm16(forms.ModelForm):
    class Meta:
        model = LineContract
        fields = [
            'full_status', 'comment_1',
            'executor'
        ]


class LetterPostForm(forms.ModelForm):

    class Meta:
        model = Letters
        fields = '__all__'
        widgets = {
            'date': forms.SelectDateWidget()
        }


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
            'executor', 'line_contract'
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
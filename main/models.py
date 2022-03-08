import numbers
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

from contract.models import LineContract


class Line(models.Model):
    device_type = models.CharField(max_length=255, blank=False, verbose_name="Тип изделия")
    device_name = models.CharField(max_length=255, blank=False, verbose_name="Наименование")
    dec_number = models.CharField(null=True, max_length=255, blank=True, verbose_name="Децимальный номер")
    number = models.CharField(max_length=255, verbose_name="Номер")
    quantity = models.IntegerField(blank=False, verbose_name="Количество")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    date_start = models.DateField(blank=False, verbose_name="Дата начала испытаний")
    date_stop_expected = models.DateField(blank=False, verbose_name="Ожидаемая дата завершения")
    date_stop = models.DateField(null=True, blank=True, verbose_name="Дата завершения испытаний")
    test_type = models.ForeignKey('TestType',  on_delete=models.PROTECT, verbose_name="Вид испытаний")
    executor = models.ForeignKey(User, editable=True, on_delete=models.PROTECT, verbose_name="Исполнитель") 
    cats = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Статус")
    act_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="Номер акта")
    customer = models.CharField(max_length=255, blank=True, null=True, verbose_name="Заказчик")
    comment = models.CharField(max_length=255, blank=True, null=True, verbose_name="Комментарий")
    act = models.FileField(upload_to='acts/', blank=True, null=True,  verbose_name="Акт")
    programm = models.FileField(upload_to='programms/', blank=True, null=True, verbose_name="Программа")
    
    def __str__(self):
        return self.device_name

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_id': self.pk})

    def get_abs_url_eq_add(self):
        return reverse('add_eq_work', kwargs={'post_id': self.pk})

    class Meta:
        verbose_name = 'Изделие'
        verbose_name_plural = 'Изделия'
        ordering = ['-id']


class EquipmentWork(models.Model):
    line_id = models.ForeignKey(Line, null=True, blank=True, editable=True, on_delete=models.PROTECT,
                                verbose_name="Испытание")
    line_contract = models.ForeignKey(LineContract, null=True, blank=True, editable=True,
                                      on_delete=models.PROTECT, verbose_name="Договорное испытание")
    eq_name = models.ForeignKey('Equipment', on_delete=models.PROTECT, verbose_name="Оборудование")
    mode = models.ForeignKey('Mode', on_delete=models.PROTECT, verbose_name="Режим")
    date_start = models.DateField(verbose_name="Дата включения")
    date_stop = models.DateField(verbose_name="Дата выключения")
    work_time = models.IntegerField(verbose_name="Время работы")
    executor = models.ForeignKey(User, editable=True, on_delete=models.PROTECT, verbose_name="Исполнитель")

    class Meta:
        verbose_name = 'Наработка'
        verbose_name_plural = 'Наработка'
        ordering = ['eq_name']


class Equipment(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Испытательное оборудование")
    number = models.CharField(max_length=100, db_index=True, verbose_name="Заводской номер")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Испытательное оборудование'
        verbose_name_plural = 'Испытательное оборудование'
        ordering = ['name']


class Mode(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Режим")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Режим'
        verbose_name_plural = 'Режимы'
        ordering = ['name']


class Category(models.Model): #Класс Текущие, Завершенные
    name = models.CharField(max_length=100, db_index=True, verbose_name="Статус")
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статус'
        ordering = ['id']


class TestType(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Вид испытаний")
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('test_type', kwargs={'test_type__id': self.pk})

    class Meta:
        verbose_name = 'Вид испытаний'
        verbose_name_plural = 'Вид испытаний'
        ordering = ['id']
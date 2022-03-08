from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class LineContract(models.Model):
    # YELLOW BACKGROUND
    # AddPostForm1
    organization = models.ForeignKey('Organization',  on_delete=models.PROTECT, verbose_name="Организация")
    device = models.CharField(max_length=127, db_index=True, verbose_name="Наименование изделия")
    enter_number = models.CharField(max_length=127, verbose_name="Входящий номер")
    request_date = models.DateField(verbose_name="Дата заявки")
    # AddPostForm2
    customer_out_number = models.CharField(blank=True, null=True, max_length=127,
                                           verbose_name="Исходящий номер заказчика")
    customer_out_date = models.DateField(blank=True, null=True,  verbose_name="Дата исходящего письма заказчика")
    customer_phone = models.CharField(blank=True, null=True, max_length=127, verbose_name="Контакты заказчика")
    # LETTERS
    # EQUIPMENT WORK
    # AddPostForm3
    official_memo = models.CharField(blank=True, null=True, max_length=127, verbose_name="Служебная записка")
    official_memo_date = models.DateField(blank=True, null=True, verbose_name="Дата СЗ")
    # AddPostForm4
    personal_time = models.FloatField(blank=True, null=True, verbose_name="Время занятости персонала")
    personal_time_spz = models.FloatField(blank=True, null=True, verbose_name="Время занятости согл. ШПЗ")
    personal_time_vp = models.FloatField(blank=True, null=True, verbose_name="Время занятости согл. ВП")
    # AddPostForm5
    expected_test_date = models.DateField(blank=True, null=True, verbose_name="Плановая дата испытания")
    # AddPostForm6
    notification_date = models.DateField(blank=True, null=True, verbose_name="Дата оповещения")
    notification_name = models.CharField(blank=True, null=True, max_length=127, verbose_name="Заказчик")
    # WHITE BACKGROUND
    # AddPostForm7
    status = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Статус испытаний")
    comment = models.CharField(blank=True, null=True, max_length=255, verbose_name="Примечания")
    # BLUE BACKGROUND
    # AddPostForm8
    expected_cost = models.FloatField(blank=True, null=True, verbose_name="Ориентировочная стоимость (руб)")
    fact_cost = models.FloatField(blank=True, null=True, verbose_name="Фактическая стоимость (руб)")
    # AddPostForm9
    bill = models.CharField(blank=True, null=True, max_length=127, verbose_name="Договор (Счет)")
    bill_date = models.DateField(blank=True, null=True, verbose_name="Дата договора")
    bill_date_signing = models.DateField(blank=True, null=True, verbose_name="Дата подписания договора")
    bill_date_final = models.DateField(blank=True, null=True, verbose_name="Дата окончания договора")
    in_gov_contract_from = models.DateField(blank=True, null=True, verbose_name="Дата окончания договора")
    # LAVENDER BACKGROUND
    # AddPostForm10
    price_protocol = models.CharField(blank=True, null=True, max_length=127,
                                      verbose_name="Протокол согласования цены/ с/з о цене")
    RKM_request = models.CharField(blank=True, null=True, max_length=127,
                                      verbose_name="Запрос ОЦО в 146 ВП о предоставлении РКМ")
    deal_number = models.CharField(blank=True, null=True, max_length=127, verbose_name="№ папки/дела")
    price_letter_number = models.CharField(blank=True, null=True, max_length=127,
                                           verbose_name="Наше исходящее письмо о цене")
    out_letter_number = models.CharField(blank=True, null=True, max_length=127,
                                           verbose_name="№ нашего исх. (об отправке договорного документа)")
    send_date = models.DateField(blank=True, null=True, verbose_name="Дата отправки договорного документа")
    # AddPostForm11
    bill_number = models.CharField(blank=True, null=True, max_length=127, verbose_name="№  счета на оплату")
    pay_bill_date = models.DateField(blank=True, null=True, verbose_name="Дата счета на оплату")
    # AddPostForm12
    pp_number = models.CharField(blank=True, null=True, max_length=127, verbose_name="№ П/П")
    pp_date = models.DateField(blank=True, null=True, verbose_name="Дата П/П")
    # AddPostForm13
    service_act_number = models.CharField(blank=True, null=True, max_length=127, verbose_name="№ акта оказанных услуг")
    service_act_date = models.DateField(blank=True, null=True, verbose_name="Дата акта оказанных услуг")
    # AddPostForm14
    bill_facture = models.CharField(blank=True, null=True, max_length=127, verbose_name="Счет-фактура")
    bill_facture_date = models.DateField(blank=True, null=True, verbose_name="Дата счет-фактуры")
    # AddPostForm15
    spz = models.CharField(blank=True, null=True, max_length=127, verbose_name="ШПЗ")
    spz_date = models.DateField(blank=True, null=True, verbose_name="Срок действия ШПЗ")
    # AddPostForm16
    full_status = models.ForeignKey('Category', related_name='full_status', on_delete=models.PROTECT,
                                    verbose_name="Статус всей заявки")
    comment_1 = models.CharField(blank=True, null=True, max_length=255, verbose_name="Примечание")
    executor = models.ForeignKey(User, editable=True, on_delete=models.PROTECT, verbose_name="Ответственный за заявку")

    def __str__(self):
        return self.device

    def get_absolute_url(self):
        return reverse('contract_post', kwargs={'post_id': self.pk})

    # def get_abs_url_eq_add(self):
    #     return reverse('add_eq_work', kwargs={'post_id': self.pk})

    class Meta:
        verbose_name = 'Изделие'
        verbose_name_plural = 'Изделия'
        ordering = ['-id']


class Organization(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Организации")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        ordering = ['name']


# add file?
class Letters(models.Model):
    line_contract = models.ForeignKey(LineContract, on_delete=models.PROTECT, verbose_name="Договор")
    # in / out
    letter_status = models.ForeignKey('LetterStatus', on_delete=models.PROTECT, verbose_name="Статус письма")
    number = models.CharField(max_length=100, blank=False, db_index=True, verbose_name="Номер письма")
    date = models.DateField(blank=False, verbose_name="Дата письма")

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'
        ordering = ['line_contract']


class LetterStatus(models.Model):
    # in / out
    name = models.CharField(max_length=100, verbose_name="Статус письма")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус письма'
        verbose_name_plural = 'Статусы писем'
        ordering = ['name']


class Category(models.Model):  # Класс Текущие, Завершенные
    name = models.CharField(max_length=100, db_index=True, verbose_name="Статус")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_id': self.pk})

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статус'
        ordering = ['id']
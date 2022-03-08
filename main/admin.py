from django.contrib import admin

from .models import *

class LineAdmin(admin.ModelAdmin):
    list_display = ('id', 'device_name', 'date_start', 'date_stop',  'executor', 'test_type')
    list_display_links = ('id', 'device_name')
    search_fields = ['device_name']
    list_editable = ('test_type', 'date_start', 'date_stop', 'executor')
    list_filter = ('device_name', 'date_start', 'date_stop', 'test_type', 'executor')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


class EquimentWorkAdmin(admin.ModelAdmin):
    list_display = ('id', 'eq_name', 'date_start', 'date_stop', 'work_time', 'line_id_id', 'line_contract_id')
    list_display_links = ('id', 'eq_name')
    search_fields = ['eq_name__name', 'line_id_id__id', 'line_id_id__device_name']
    list_editable = ('date_start', 'date_stop', 'work_time')
    list_filter = ('eq_name', 'date_start', 'date_stop')
    

class EquimentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'number')
    list_display_links = ('id', 'name')
    search_fields = ['name', 'number']


class TestTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)

class ModeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    

admin.site.register(Line, LineAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Equipment, EquimentAdmin)
admin.site.register(EquipmentWork, EquimentWorkAdmin)
admin.site.register(TestType, TestTypeAdmin)
admin.site.register(Mode, ModeAdmin)


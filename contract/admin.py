from django.contrib import admin

from .models import *


class LineContractAdmin(admin.ModelAdmin):
    list_display = ('id', 'organization', 'device', 'enter_number')
    list_display_links = ('id', 'organization')
    search_fields = ['organization']
    list_editable = ('device',)
    list_filter = ('organization',)


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


class LettersAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'letter_status', 'date')
    list_display_links = ('id', 'number')
    search_fields = ('number', 'line_contract')


class LetterStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


admin.site.register(LineContract, LineContractAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Letters, LettersAdmin)
admin.site.register(LetterStatus, LetterStatusAdmin)
admin.site.register(Category, CategoryAdmin)

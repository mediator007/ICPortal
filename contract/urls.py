from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', LineContractHome.as_view(), name='contract'),
    path('complete/', CompleteOrganizations.as_view(), name='complete_contracts'),
    # org = organization.pk
    path('complete/<int:org>/', Complete.as_view(), name='complete'),
    path('contract_post/<int:post_id>/', ShowPost.as_view(), name='contract_post'),
    path('addpage/', add_page, name='contract_addpage'),
    # id = post.pk, n = AddPostForm number
    path('contract_post/editline/<int:id>/<int:n>/', edit_line, name='editline'),
    path('search/', search, name='search'),
    # num = post.pk for auto-input of 'line_contract' field
    path('addletter/<int:num>/', add_letter, name='addletter'),
    # num = post.pk, num1 = letter.pk
    path('editletter/<int:num>/<int:num1>/', edit_letter, name='editletter'),
    # num = post.pk
    path('addequipment/<int:num>/', add_equipment_work, name='addequipment'),
    # num = post.pk, num1 = eqwork.pk
    path('editequipment/<int:num>/<int:num1>/', edit_equipment_work, name='editEquipmentWork')
]

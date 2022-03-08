from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', LineHome.as_view(), name='home'),
    path('addpage/', add_page, name='add_page'),
    path('addEquipmentWork/<int:id>/', add_equipment_work, name='addEquipmentWork'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('post/<int:post_id>/', ShowPost.as_view(), name='post'),
    path('editLine/<int:id>/', editLine, name='editLine'),
    # id - , id1 -
    path('editEquipmentWork/<int:id>/<int:id1>/', editEquipmentWork, name='editEquipmentWork'),
    path('search_results/', search, name='search_results'),
    path('complete/', complete, name='complete'),
    path('complete/<str:date>', complete_date, name='complete_date'),
    path('reports/', reports, name='reports'),
    path('reports/<int:id>/', reports_eq, name='reports_eq'),
    path('reports/<int:id>/<str:date>', report_date, name='report_date'),
    path('getactnumber/<int:id>/', get_act_number, name='getactnumber')
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('charts/', views.charts, name = 'charts'),
    path('get-data/', views.get_data_view, name = 'get_data'),
    path('save-table/', views.save_table, name = 'save_table'),
    path('change-api/', views.change_api, name = 'change_api'),
]

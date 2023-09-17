from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('charts/', views.charts, name = 'charts'),
    path('get-data/', views.get_data_view, name = 'get_data')
]

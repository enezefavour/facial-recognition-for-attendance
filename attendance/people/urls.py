from django.urls import path
from . import views
from datetime import date




#URL Conf
urlpatterns  = [
    path('', views.index, name='people_index'),
    path('details/', views.detail, name='people_detail'),
    path('attendance/', views.show_attendance, name='show_attendance'),
    path('advanced_search/', views.search, name='advanced_search')
]
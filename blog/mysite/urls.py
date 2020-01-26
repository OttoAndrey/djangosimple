from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('testpage/', views.testpage, name='testpage'),
]


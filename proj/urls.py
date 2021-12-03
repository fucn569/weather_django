from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.wait, name='wait'),
    path('home/', views.home, name='home'),
    path('city/', views.city, name='city'),
    path('nav/', views.nav, name='nav'),
]

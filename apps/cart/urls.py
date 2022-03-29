from django.urls import path
from django.utils.translation import gettext 

from . import views

urlpatterns = [
    path('', views.cart_detail, name='cart'),
    path('success/', views.success, name='success')
]
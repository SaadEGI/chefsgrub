#
#

from django.urls import path

#
#

from . import views

#
#

urlpatterns = [
    path('', views.frontpage, name='frontpage'),
    path('contact/', views.contact, name='contact'),
    path('home2/', views.home, name='home'),
    path('comingsoon/', views.comingsoon, name='comingsoon'),

]
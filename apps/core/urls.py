from django.utils.translation import gettext 
#
#

from django.urls import path

#
#

from . import views

#
#
app_name = "apps.core"

urlpatterns = [
    path('', views.frontpage, name='frontpage'),
    path('contact/', views.contact, name='contact'),
    path('home2/', views.home, name='home'),
    path('aboutus/', views.aboutus, name='aboutus'),

]
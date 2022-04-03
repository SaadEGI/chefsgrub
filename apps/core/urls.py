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
    path('aboutus/', views.aboutus, name='about'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('faq/', views.faq, name='faq'),

]

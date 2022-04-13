#
#

from django.urls import path

#
#

from . import views

#
#

urlpatterns = [
    path('browse/', views.frontpage, name='frontpage'),
    path('contact/', views.contact, name='contact'),
    path('', views.home, name='home'),
    path('comingsoon/', views.comingsoon, name='comingsoon'),
    path('about/', views.about, name='about'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('faq/', views.faq, name='faq'),
    path('confirm/', views.confirm, name='confirm'),
    path('delete/', views.delete, name='delete'),

]

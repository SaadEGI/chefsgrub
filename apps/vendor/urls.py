from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('become-vendor/', views.become_vendor, name='become_vendor'),
    path('vendor-admin/', views.vendor_admin, name='vendor_admin'),
    path('add-product/', views.add_product, name='add_product'),
    path('edit-vendor/', views.edit_vendor, name='edit_vendor'),
    path('edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='vendor/login.html'), name='login'),
    path('', views.vendors, name='vendors'),
    path('<int:vendor_id>/', views.vendor, name='vendor'),



    path('chef/become-chef/', views.become_chef, name='become-chef'),

    path('chef/sign-in/', auth_views.LoginView.as_view(
        template_name='chef/sign_in.html', next_page='/vendors/chef'), name='chef-sign-in'),


    path('chef/', views.chef_home, name='chef-home'),
    path('chef/order/', views.chef_order, name='chef-order'),
    path('chef/meal/', views.chef_meal, name='chef-meal'),  # TODO
    path('chef/customers/', views.chef_customers, name='chef-customers'),  # TODO
    path('chef/report/', views.chef_report, name='chef-report'),
    path('chef/account/', views.chef_account, name='chef-account'),
    path('chef/sign-out', auth_views.LogoutView.as_view(),
         {'next_page': '/'}, name='chef-sign-out'),
    path('chef/meal/add/', views.chef_add_meal, name='chef-add-meal'),
    path('chef/meal/edit/', views.chef_edit_meal, name='chef-edit-meal'),
]

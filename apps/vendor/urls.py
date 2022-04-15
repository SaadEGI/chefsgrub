from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf.urls.i18n import i18n_patterns
from . import views 

app_name = "vendor"
urlpatterns = [
    # Views for chefs @ /chef
    path("become-chef/", views.become_chef, name="become-chef"),
    path(
        "sign-in/",
        auth_views.LoginView.as_view(template_name="chef/sign_in.html", next_page="/chef/order"),
        name="chef-sign-in",
    ),
    path("chef-admin/", views.chef_admin, name="chef-admin"),
    path("order/", views.chef_order, name="chef-order"),
    path("meal/", views.chef_meal, name="chef-meal"),  # TODO
    path("customers/", views.chef_customers, name="chef-customers"),  # TODO
    path("report/", views.chef_report, name="chef-report"),
    path("account/", views.chef_account, name="chef-account"),
    path("sign-out", auth_views.LogoutView.as_view(), {"next_page": "/"}, name="chef-sign-out"),
    path("meal/add/", views.chef_add_meal, name="chef-add-meal"),
    path("meal/edit/<int:meal_id>", views.chef_edit_meal, name="chef-edit-meal"),
    # Views for customers @ /chef
    path("<str:vendorName>/", views.vendor, name="vendor"),
    path("", views.vendors, name="vendors"),
]

i18n_patterns
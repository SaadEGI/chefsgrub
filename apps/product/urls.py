from django.utils.translation import gettext 
from django.urls import path

from . import views
app_name = "apps.product"

urlpatterns = [
    path('search/', views.search, name='search'),
    path('<slug:category_slug>/<slug:product_slug>/', views.product, name='product'),
    path('<slug:category_slug>/', views.category, name='category')
]
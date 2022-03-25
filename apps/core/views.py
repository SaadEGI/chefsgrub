from django.shortcuts import render

from apps.product.models import Product
from apps.vendor.models import Vendor

def frontpage(request):
    newest_products = Product.objects.all()[0:8]
    vendorsall = Vendor.objects.all()
    ramadan_products = Product.objects.filter(category=1)

    return render(request, 'core/frontpage.html',{'ramadan_products':ramadan_products,'newest_products': newest_products, 'vendorsall':vendorsall})

def contact(request):
    return render(request, 'core/contact.html')

def home(request):
    return render(request, 'core/home2.html', {})

def comingsoon(request):
    return render(request, 'core/coming-soon.html', {})
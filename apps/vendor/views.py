from . import forms
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404

from .models import Vendor
from apps.product.models import Product, ProductImage

from .forms import ProductForm, ProductImageForm

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from apps.product.forms import AddToCartForm
from apps.product.models import Category, Product

from apps.order.models import *
from apps.cart.cart import Cart
from .forms import RegisterChefForm
from apps.order.utilities import *




def vendors(request):
    vendors = Vendor.objects.all()

    return render(request, 'vendor/chef.html', {'vendors': vendors})

@csrf_exempt
def vendor(request, vendorName):
    vendor = get_object_or_404(Vendor, pk=vendorName)
    cart = Cart(request)
    imagesstring = '{"thumbnail": "%s","image": "%s", "id": "mainimage"},' % (
        vendor.get_thumbnail(), vendor.logo.url)
    print(imagesstring)
    if request.method == 'POST':
        form = AddToCartForm(request.POST)

        if form.is_valid():
            quantity = 1
            # product.id =1
            product_id = form.cleaned_data['product_id']

            # form.cleaned_data['quantity']

            cart.add(product_id=product_id, quantity=quantity, update_quantity=False)

            messages.success(request, 'The product was added to the cart')

    else:
        form = AddToCartForm()

    return render(request, 'vendor/chef.html', {'form': form ,'vendor': vendor,'imagesstring': "[" + imagesstring.rstrip(',') + "]"})




def become_chef(request):
    if request.method == 'POST':
        form = RegisterChefForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            chef = Vendor.objects.create(name=user.username, created_by=user)

            return redirect("vendor:chef-order")
    else:
        form = RegisterChefForm()

    return render(request, 'chef/sign_up.html', {'form': form})


@login_required(login_url='/chef/sign-in/')
def chef_admin(request):
    return redirect("vendor:chef-order")


@login_required(login_url='/chef/sign-in/')
def chef_order(request):
    chef = request.user.vendor
    orders = chef.orders.all()
    if 'btnform1' in request.POST:

        order = request.POST.get("order")
        sts = 'confirmed'
        order.status = sts
        print("testyy")

        return redirect("vendor:chef_order")
    if 'btnform2' in request.POST:

        order = request.POST.get("order")
        sts = 'cancelled'
        order.status = sts

        return redirect("vendor:chef_order")




    return render(request, 'chef/order.html', {'orders': orders,'orders': orders, 'chef': chef})


@login_required(login_url='/chef/sign-in/')
def chef_meal(request):
    chef = request.user.vendor
    meals = Product.objects.filter(
        vendor=chef).order_by("-id")
    return render(request, 'chef/meal.html', {"meals": meals, 'chef': chef}) # 


@login_required(login_url='/chef/sign-in/')
def chef_customers(request):
    return redirect('/')
# @login_required(login_url='/chef/sign-in/')
# def chef_customers(request):

#     customers = Customer.objects.annotate(total_order=Count(
#         Case(When(order__chef=request.user.chef,
#                   then=1)))).order_by("-total_order")

#     all_customers = [
#         customer for customer in customers if customer.total_order > 0
#     ]

#     return render(request, 'chef/customers.html',
#                   {"all_customers": all_customers})


@login_required(login_url='/chef/sign-in/')
def chef_account(request):
    user_form = forms.UserFormForEdit(instance=request.user)
    chef_form = forms.ChefForm(instance=request.user)
    chef = request.user.vendor

    if request.method == "POST":
        user_form = forms.UserFormForEdit(request.POST, instance=request.user)
        chef_form = forms.ChefForm(request.POST,
                                   request.FILES,
                                   instance=request.user.vendor)

        if user_form.is_valid() and chef_form.is_valid():
            user_form.save()
            chef_form.save()

    return render(request, 'chef/account.html', {
        "user_form": user_form,
        'chef': chef,
        "chef_form": chef_form #TODO: change forms to accomodate the model used
# TODO: hook it up, take notes from edit_vendor
    })


@login_required(login_url='/chef/sign-in/')
def chef_add_meal(request):
    chef = request.user.vendor
    if request.method == 'POST':
        form = forms.ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user.vendor
            product.slug = slugify(product.title)
            product.save()

            return redirect("vendor:chef-meal")
    else:
        form = forms.ProductForm()

    return render(request, 'chef/add_meal.html', {
        'chef': chef,
        'form': form
    })
@login_required(login_url='/chef/sign-in/')
def chef_report(request):
    return render(request, 'chef/report.html', {}) # TODO: get the actual report to work

@login_required(login_url='/chef/sign-in/')
def chef_edit_meal(request, meal_id):
    form = forms.ProductForm(instance=Product.objects.get(id=meal_id))

    if request.method == "POST":
        form = forms.ProductForm(request.POST,
                        request.FILES,
                        instance=Product.objects.get(id=meal_id))
        if form.is_valid():
            form.save()
            return redirect(chef_meal)

    return render(request, 'chef/edit_meal.html', {"form": form}) # TODO: hook it up, take notes from edit_product


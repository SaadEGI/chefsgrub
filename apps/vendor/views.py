from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.utils.text import slugify
from django.shortcuts import render, redirect, get_object_or_404
from . import forms

from .models import Vendor
from apps.product.models import Product, ProductImage
from apps.order.models import Order, OrderItem

from . import forms


def become_vendor(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            vendor = Vendor.objects.create(name=user.username, created_by=user)

            return redirect('frontpage')
    else:
        form = UserCreationForm()

    return render(request, 'vendor/become_vendor.html', {'form': form})


@login_required
def vendor_admin(request):
    vendor = request.user.vendor
    products = vendor.products.all()
    orders = vendor.orders.all()

    for order in orders:
        order.vendor_amount = 0
        order.vendor_paid_amount = 0
        order.fully_paid = True

        for item in order.items.all():
            if item.vendor == request.user.vendor:
                if item.vendor_paid:
                    order.vendor_paid_amount += item.get_total_price()
                else:
                    order.vendor_amount += item.get_total_price()
                    order.fully_paid = False

    return render(request, 'vendor/vendor_admin.html', {'vendor': vendor, 'products': products, 'orders': orders})


@login_required
def add_product(request):
    if request.method == 'POST':
        form = forms.ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user.vendor
            product.slug = slugify(product.title)
            product.save()

            return redirect('vendor_admin')
    else:
        form = forms.ProductForm()

    return render(request, 'vendor/add_product.html', {'form': form})


@login_required
def edit_product(request, pk):
    vendor = request.user.vendor
    product = vendor.products.get(pk=pk)

    if request.method == 'POST':
        form = forms.ProductForm(request.POST, request.FILES, instance=product)
        image_form = forms.ProductImageForm(request.POST, request.FILES)

        if image_form.is_valid():
            productimage = image_form.save(commit=False)
            productimage.product = product
            productimage.save()

            return redirect('vendor_admin')

        if form.is_valid():
            form.save()

            return redirect('vendor_admin')
    else:
        form = forms.ProductForm(instance=product)
        image_form = forms.ProductImageForm()

    return render(request, 'vendor/edit_product.html', {'form': form, 'image_form': image_form, 'product': product})


@login_required
def edit_vendor(request):
    vendor = request.user.vendor

    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')

        if name:
            vendor.created_by.email = email
            vendor.created_by.save()

            vendor.name = name
            vendor.save()

            return redirect('vendor_admin')

    return render(request, 'vendor/edit_vendor.html', {'vendor': vendor})


def vendors(request):
    vendors = Vendor.objects.all()

    return render(request, 'vendor/vendors.html', {'vendors': vendors})


def vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)

    return render(request, 'vendor/vendor.html', {'vendor': vendor})


def become_chef(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            chef = Vendor.objects.create(name=user.username, created_by=user)

            return redirect('chef-order')
    else:
        form = UserCreationForm()

    return render(request, 'chef/sign_up.html', {'form': form})


@login_required(login_url='/vendors/chef/sign-in/')
def chef_home(request):
    return redirect('chef-order')


@login_required(login_url='/vendors/chef/sign-in/')
def chef_order(request):
    # if request.method == "POST":
        # order = Order.objects.get(id=request.POST["id"],
        #                           vendor=request.user.vendor)

        # if order.status == Order.COOKING:
        #     order.status = Order.READY
        #     order.save()
    chef = request.user.vendor
    orders = OrderItem.objects.filter(
    vendor=chef).order_by("-id") 
    # #TODO: fix filter

    return render(request, 'chef/order.html', {"orders": orders, 'chef': chef})


@login_required(login_url='/vendors/chef/sign-in/')
def chef_meal(request):
    chef = request.user.vendor
    meals = Product.objects.filter(
        vendor=chef).order_by("-id")
    return render(request, 'chef/meal.html', {"meals": meals, 'chef': chef}) # 


@login_required(login_url='/vendors/chef/sign-in/')
def chef_customers(request):
    return redirect('/')
# @login_required(login_url='/vendors/chef/sign-in/')
# def chef_customers(request):

#     customers = Customer.objects.annotate(total_order=Count(
#         Case(When(order__chef=request.user.chef,
#                   then=1)))).order_by("-total_order")

#     all_customers = [
#         customer for customer in customers if customer.total_order > 0
#     ]

#     return render(request, 'chef/customers.html',
#                   {"all_customers": all_customers})


@login_required(login_url='/vendors/chef/sign-in/')
def chef_account(request):
    user_form = forms.UserFormForEdit(instance=request.user)
    chef_form = forms.ChefForm(instance=request.user)
    chef = request.user.vendor

    if request.method == "POST":
        user_form = forms.UserFormForEdit(request.POST, instance=request.user)
        chef_form = forms.ChefForm(request.POST,
                                   request.FILES,
                                   instance=request.user.chef)

        if user_form.is_valid() and chef_form.is_valid():
            user_form.save()
            chef_form.save()

    return render(request, 'chef/account.html', {
        "user_form": user_form,
        'chef': chef,
        "chef_form": chef_form #TODO: change forms to accomodate the model used
# TODO: hook it up, take notes from edit_vendor
    })


@login_required(login_url='/vendors/chef/sign-in/')
def chef_add_meal(request):
    chef = request.user.vendor
    if request.method == 'POST':
        form = forms.ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user.vendor
            product.slug = slugify(product.title)
            product.save()

            return redirect('vendor_admin')
    else:
        form = forms.ProductForm()

    return render(request, 'chef/add_meal.html', {
        'chef': chef,
        'form': form
    })
@login_required(login_url='/vendors/chef/sign-in/')
def chef_report(request):
    return render(request, 'chef/report.html', {}) # TODO: get the actual report to work

@login_required(login_url='/vendors/chef/sign-in/')
def chef_edit_meal(request, meal_id):
    form = ProductForm(instance=Meal.objects.get(id=meal_id))

    if request.method == "POST":
        form = ProductForm(request.POST,
                        request.FILES,
                        instance=Meal.objects.get(id=meal_id))

        if form.is_valid():
            form.save()
            return redirect(chef_meal)

    return render(request, 'chef/edit_meal.html', {"form": form}) # TODO: hook it up, take notes from edit_product


# @login_required(login_url='/vendors/restaurant/sign-in/')
# def restaurant_report(request):
#     # Calculate revenue and number of order by current week
#     from datetime import datetime, timedelta

#     revenue = []
#     orders = []

#     # Calculate weekdays
#     today = datetime.now()
#     current_weekdays = [
#         today + timedelta(days=i)
#         for i in range(0 - today.weekday(), 7 - today.weekday())
#     ]

#     for day in current_weekdays:
#         delivered_orders = Order.objects.filter(
#             restaurant=request.user.restaurant,
#             status=Order.DELIVERED,
#             created_at__year=day.year,
#             created_at__month=day.month,
#             created_at__day=day.day)
#         revenue.append(sum(order.total for order in delivered_orders))
#         orders.append(delivered_orders.count())

#     # Top 3 Meals
#     top3_meals = Meal.objects.filter(restaurant = request.user.restaurant)\
#                      .annotate(total_order = Sum('orderdetails__quantity'))\
#                      .order_by("-total_order")[:3]

#     meal = {
#         "labels": [meal.name for meal in top3_meals],
#         "data": [meal.total_order or 0 for meal in top3_meals]
#     }

#     # Top 3 Drivers
#     top3_drivers = Driver.objects.annotate(total_order=Count(
#         Case(When(order__restaurant=request.user.restaurant,
#                   then=1)))).order_by("-total_order")[:3]

#     driver = {
#         "labels": [driver.user.get_full_name() for driver in top3_drivers],
#         "data": [driver.total_order for driver in top3_drivers]
#     }

#     # Top 3 Drivers
#     top3_customers = Customer.objects.annotate(total_order=Count(
#         Case(When(order__restaurant=request.user.restaurant,
#                   then=1)))).order_by("-total_order")[:3]

#     customer = {
#         "labels":
#         [customer.user.get_full_name() for customer in top3_customers],
#         "data": [customer.total_order for customer in top3_customers]
#     }

#     return render(
#         request, 'restaurant/report.html', {
#             "revenue": revenue,
#             "orders": orders,
#             "meal": meal,
#             "driver": driver,
#             "customer": customer
#         })


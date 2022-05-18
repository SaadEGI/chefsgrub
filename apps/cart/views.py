import json

import stripe

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from apps.cart.utils import create_new_ref_number
from django.http import JsonResponse
from apps.order.models import Order

from .cart import Cart
from .forms import CheckoutForm
from django.core import serializers

from apps.order.utilities import checkout, notify_customer, notify_vendor
from django.forms.models import model_to_dict

@csrf_exempt
def payment_done(request):
    return render(request, 'cart/done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'cart/canceled.html')


def payment_process(request):
    cart = Cart(request)
    host = request.get_host()
    order = Order(request)
    return render(request, 'cart/process.html')


def cart_detail(request):
    #self.session = request.session

    someDict = {1:'s'}

    #request.session['order'] = "test"

    #order = Order(request)
    #for items in Cart
    for key, value in request.session.items():
        print('{} => {}'.format(key, value))



    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        cart = Cart(request)



        if form.is_valid():
            cart = Cart(request)
            if(form.cleaned_data['paymentmethod'] == "PayPal"):
                print("Paypal choosed")
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                phone = form.cleaned_data['phone']
                address = form.cleaned_data['address']
                zipcode = form.cleaned_data['zipcode']
                place = form.cleaned_data['place']
                paymentmethod = 'pypnt'
                status = 'pending'
                order = checkout(request, first_name, last_name, email, address, zipcode, place, phone,
                                 cart.get_total_cost(), paymentmethod,status)
                for key, value in request.session.items():
                    print('{} => {}'.format(key, value))
                request.POST[order.id]



                return redirect('cart:process')


            if (form.cleaned_data['paymentmethod'] == "Cash"):
                print("Paypal NOTT choosed")
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                phone = form.cleaned_data['phone']
                address = form.cleaned_data['address']
                zipcode = form.cleaned_data['zipcode']
                place = form.cleaned_data['place']
                paymentmethod = 'COD'
                status = 'pending'
                order = checkout(request, first_name, last_name, email, address, zipcode, place, phone,
                                 cart.get_total_cost(), paymentmethod, status)


                cart.clear()

                # notify_customer(order)
                # notify_vendor(order)

                return redirect('cart:successcash')


            # stripe.api_key = settings.STRIPE_SECRET_KEY

            # stripe_token = form.cleaned_data['stripe_token']



    else:
        form = CheckoutForm()

    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)

    if remove_from_cart:
        cart.remove(remove_from_cart)

        return redirect('cart:cart')

    if change_quantity:
        cart.add(change_quantity, quantity, True)

        return redirect('cart:cart')

    return render(request, 'cart/cart.html', {'form': form})

def successcash(request):

    return render(request, 'cart/success.html')

def success(request):
    for key, value in request.session.items():
        print('{} => {}'.format(key, value))
    #body = json.loads(request.body)
    #print('BODY', body)
    #product.
    body = json.loads(request.body)
    print('BODY:', body)
    if 'order' in request.session:
        order = request.session['order']
        order.paymentmethod="pyp"
    else:
        order = Order.objects.get(pk=2)
        order.paymentmethod = "pyp"

    #product = Product.objects.get(id=body['productId'])

    return render(request, 'cart/success.html')


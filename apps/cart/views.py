import stripe

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm

from apps.order.models import Order

from .cart import Cart
from .forms import CheckoutForm

from apps.order.utilities import checkout, notify_customer, notify_vendor


@csrf_exempt
def payment_done(request):

    return render(request, 'cart/done.html')


@csrf_exempt
def payment_canceled(request):

    return render(request, 'cart/canceled.html')


def payment_process(request):
    cart = Cart(request)
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount':  cart.get_total_cost(),
        'item_name': 'Bestellung',
        'invoice': 'ChefsGrub order',
        'currency_code': 'EUR',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('cart:done')),
        'cancel_return': 'http://{}{}'.format(host, reverse('cart:canceled')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'cart/process.html', {'form': form})

def cart_detail(request):
    cart = Cart(request)


    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        if form.is_valid():
            # stripe.api_key = settings.STRIPE_SECRET_KEY

            # stripe_token = form.cleaned_data['stripe_token']

            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            zipcode = form.cleaned_data['zipcode']
            place = form.cleaned_data['place']
            paymentmethod = 'PYP'
            order = checkout(request, first_name, last_name, email, address, zipcode, place, phone,
                             cart.get_total_cost(),paymentmethod)

            cart.clear()

            notify_customer(order)
            notify_vendor(order)

            return redirect('cart:success')

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


def success(request):
    return render(request, 'cart/success.html')
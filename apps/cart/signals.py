from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver

from .cart import Cart

from apps.order.utilities import checkout, notify_customer, notify_vendor

@receiver(valid_ipn_received)
def show_me_the_money(sender,request, **kwargs):

    cart = Cart(request)
    ipn_obj = sender
    if ipn_obj.payment_status == "Completed":
        if cart.total_cost() == ipn_obj.mc_gross:
            print("ST_PP_COMPLETED")
            first_name = ipn_obj.first_name
            last_name = ipn_obj.last_name
            email = ipn_obj.payer_email
            phone = ipn_obj.contact_phone
            address = ipn_obj.address_street
            zipcode = ipn_obj.address_zip
            place = ipn_obj.address_city
            paymentmethod = 'Paypal'
            order = checkout(request, first_name, last_name, email, address, zipcode, place, phone,
                             cart.get_total_cost(), paymentmethod)

            cart.clear()

            notify_customer(order)
            notify_vendor(order)


valid_ipn_received.connect(show_me_the_money)

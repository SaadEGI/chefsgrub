from django.shortcuts import render

from apps.product.models import Product
from apps.vendor.models import Vendor
from .forms import ContactForm

from django.core.mail import send_mail
import http.client
import requests
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Subscriber
from .forms import SubscriberForm
import random
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def confirm(request):
    sub = Subscriber.objects.get(email=request.GET['email'])
    if sub.conf_num == request.GET['conf_num']:
        sub.confirmed = True
        sub.save()
        return render(request, 'core/home-2.html', {'email': sub.email, 'action': 'confirmed'})
    else:
        return render(request, 'core/home-2.html', {'email': sub.email, 'action': 'denied'})

def delete(request):
    sub = Subscriber.objects.get(email=request.GET['email'])
    if sub.conf_num == request.GET['conf_num']:
        sub.delete()
        return render(request, 'core/home-2.html', {'email': sub.email, 'action': 'unsubscribed'})
    else:
        return render(request, 'core/home-2.html', {'email': sub.email, 'action': 'denied'})



# Helper Functions
def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)

@csrf_exempt
def home(request):
    if request.method == 'POST':
        sub = Subscriber(email=request.POST['email'], conf_num=random_digits())
        sub.save()
        message = Mail(
            from_email=settings.FROM_EMAIL,
            to_emails=sub.email,
            subject='Newsletter Confirmation',
            html_content='Thank you for signing up for my email newsletter! \
                Please complete the process by \
                <a href="{}confirm/?email={}&conf_num={}"> clicking here to \
                confirm your registration</a>.'.format(request.build_absolute_uri(''),
                                                    sub.email,
                                                    sub.conf_num))
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        return render(request, 'core/home-2.html', {'email': sub.email, 'action': 'added', 'form': SubscriberForm()})
    else:
        return render(request, 'core/home-2.html', {'form': SubscriberForm()})



def frontpage(request):
    newest_products = Product.objects.all()[0:8]
    vendorsall = Vendor.objects.all()
    ramadan_products = Product.objects.filter(category=2)

    return render(request, 'core/frontpage.html',{'ramadan_products':ramadan_products,'newest_products': newest_products, 'vendorsall':vendorsall})


def about(request):
    return render(request, 'core/About.html')

def privacy(request):
    return render(request, 'core/privacy.html')

def terms(request):
    return render(request, 'core/terms.html')

def faq(request):
    return render(request, 'core/faq.html')
#
# def home(request):
#     return render(request, 'core/home-2.html', {})

def comingsoon(request):
    return render(request, 'core/coming-soon.html', {})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry from "
            body = {
                'full_name': form.cleaned_data['full_name'],
                'email': form.cleaned_data['email_address'],
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message, form.email_address, ['strtporg@gmail.com'],
                          fail_silently=False)

            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect("core:frontpage")

    form = ContactForm()
    return render(request, "core/contact.html", {'form': form})


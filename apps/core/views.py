from django.shortcuts import render

from apps.product.models import Product
from apps.vendor.models import Vendor
from .forms import ContactForm

from django.core.mail import send_mail
import http.client
import requests
import json
SENDGRID_API_KEY = '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'



def frontpage(request):
    newest_products = Product.objects.all()[0:8]
    vendorsall = Vendor.objects.all()
    ramadan_products = Product.objects.filter(category=2)

    return render(request, 'core/frontpage.html',{'ramadan_products':ramadan_products,'newest_products': newest_products, 'vendorsall':vendorsall})


def aboutus(request):
    return render(request, 'core/about.html')

def home(request):
    return render(request, 'core/home2.html', {})

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
            return redirect("frontpage")

    form = ContactForm()
    return render(request, "core/contact.html", {'form': form})

def subscriber_add(request):
    if request.method == 'POST':
        try:
            conn = http.client.HTTPSConnection("api.sendgrid.com")
            email = request.POST.get('subscriber-email')
            payload = json.dumps({"contacts": [{"email": email}]})
            headers = {
                'authorization': "Bearer %s" % SENDGRID_API_KEY,
                'content-type': "application/json"
            }
            conn.request("PUT", "/v3/marketing/contacts", payload, headers)
            res = conn.getresponse()
            data = res.read()
            print(data.decode("utf-8"))
        except Exception as e:
            print(e.message)
    return redirect('/')
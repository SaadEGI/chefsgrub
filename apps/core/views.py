from django.shortcuts import render

from apps.product.models import Product
from apps.vendor.models import Vendor
from .forms import ContactForm

from django.core.mail import send_mail


def frontpage(request):
    newest_products = Product.objects.all()[0:8]
    vendorsall = Vendor.objects.all()
    ramadan_products = Product.objects.filter(category=1)

    return render(request, 'core/frontpage.html',{'ramadan_products':ramadan_products,'newest_products': newest_products, 'vendorsall':vendorsall})


def aboutus(request):
    return render(request, 'core/About.html')

def home(request):
    return render(request, 'core/home-2.html', {})


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
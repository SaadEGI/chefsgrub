from django import forms
PAYMENTCHOISE =(
    ("Cash", "Cash"),
    ("PayPal", "Paypal"),
)

class CheckoutForm(forms.Form):

    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=255)
    phone = forms.CharField(max_length=255)
    address = forms.CharField(max_length=255)
    zipcode = forms.CharField(max_length=255)
    place = forms.CharField(max_length=255)
    paymentmethod = forms.ChoiceField(choices = PAYMENTCHOISE)


class PaymentMethod(forms.Form):

    paymentmethod2 = forms.ChoiceField(choices = PAYMENTCHOISE)

# from django.forms import forms.ModelForm, forms.CharField
from django import forms
from . import models
from apps.product.models import Product, ProductImage
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'image', 'title', 'description', 'price']

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']
class ChefForm(forms.ModelForm):
    class Meta:
        model = models.Vendor # Restaurant
        fields = ("name", "phone", "address", "logo")


class UserFormForEdit(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")



class UserForm(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.widgets.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "password", "first_name", "last_name", "email")

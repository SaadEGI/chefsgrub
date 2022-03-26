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
        fields = ("phone", "address", "logo") # TODO: cos "name" field is primary key on the Vendor model, it is sensitive. Updating it should be
        # done in the right way. If being a PK prevents it from being updated without creating problems, a new PK should be used instead


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

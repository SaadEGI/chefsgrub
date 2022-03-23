from django import forms

class AddToCartForm(forms.Form):
    quantity = 1
    product_id =forms.IntegerField()
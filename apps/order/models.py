from django.db import models

from apps.product.models import Product
from apps.vendor.models import Vendor

class Order(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2)
    vendors = models.ManyToManyField(Vendor, related_name='orders')
    id = models.AutoField(primary_key=True)
    class paymentmethod(models.TextChoices):
        cod = '1', "COD"
        pyp = '2', "Paypal paid"
        pypnt = '3', "Paypal Not paid"

    paymentmethod = models.CharField(
        max_length=5,
        choices=paymentmethod.choices,
        default=paymentmethod.cod
    )

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.first_name

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, related_name='items', on_delete=models.CASCADE)
    vendor_paid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)
    id = models.AutoField(primary_key=True)
    
    def __str__(self):
        return '%s' % self.id
    
    def get_total_price(self):
        return self.price * self.quantity
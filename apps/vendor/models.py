from django.contrib.auth.models import User
from django.db import models

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=500, default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=500, default=None, blank=True, null=True)
    created_by = models.OneToOneField(User, related_name='vendor', on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_balance(self):
        items = self.items.filter(vendor_paid=False, order__vendors__in=[self.id])
        return sum((item.product.price * item.quantity) for item in items)
    
    def get_paid_amount(self):
        items = self.items.filter(vendor_paid=True, order__vendors__in=[self.id])
        return sum((item.product.price * item.quantity) for item in items)
# class Chef(models.Model):
#     user = models.OneToOneField(User,
#                                 on_delete=models.CASCADE,
#                                 related_name='chef')
#     name = models.CharField(max_length=500)
#     phone = models.CharField(max_length=500, default=None, blank=True, null=True)
#     address = models.CharField(max_length=500, default=None, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     id = models.AutoField(primary_key=True)
#     class Meta:
#         ordering = ['name']
    
#     def __str__(self):
#         return self.name
    
#     def get_balance(self):
#         items = self.items.filter(vendor_paid=False, order__vendors__in=[self.id])
#         return sum((item.product.price * item.quantity) for item in items)
    
#     def get_paid_amount(self):
#         items = self.items.filter(vendor_paid=True, order__vendors__in=[self.id])
#         return sum((item.product.price * item.quantity) for item in items)
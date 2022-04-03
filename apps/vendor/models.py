from django.contrib.auth.models import User
from django.db import models
from io import BytesIO
from PIL import Image

from django.core.files import File

class Vendor(models.Model):
    name = models.CharField(max_length=255, unique=True, primary_key=True)
    phone = models.CharField(max_length=500, default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=500, default=None, blank=True, null=True)
    created_by = models.OneToOneField(User, related_name='vendor', on_delete=models.CASCADE)
    # id = models.AutoField(primary_key=True)
    logo = models.ImageField(upload_to='uploads/', default=None, blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)

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

    def get_thumbnail(self):
            if self.thumbnail:
                return self.thumbnail.url
            else:
                if self.logo:
                    self.thumbnail = self.make_thumbnail(self.logo)
                    self.save()

                    return self.thumbnail.url
                else:
                    return "https://via.placeholder.com/240x180.jpg"

    def make_thumbnail(self, logo, size=(300, 200)):
            # img = Image.open(image)
            # img.convert("RGB")
            img = logo.open(logo)
            rgb_img = img.convert('RGB')
            rgb_img.thumbnail(size)

            thumb_io = BytesIO()
            rgb_img.save(thumb_io, "JPEG", quality=85)

            thumbnail = File(thumb_io, name=logo.name)

            return thumbnail

class VendorImage(models.Model):
        vendor = models.ForeignKey(Vendor, related_name="images", on_delete=models.CASCADE)
        image = models.ImageField(upload_to="uploads/", blank=True, null=True)
        thumbnail = models.ImageField(upload_to="uploads/", blank=True, null=True)

        def get_thumbnail(self):
            if self.thumbnail:
                return self.thumbnail.url
            else:
                if self.image:
                    self.thumbnail = self.make_thumbnail(self.image)
                    self.save()

                    return self.thumbnail.url
                else:
                    return "https://via.placeholder.com/240x180.jpg"

        def make_thumbnail(self, image, size=(300, 200)):
            img = Image.open(image)
            img.convert("RGB")
            img.thumbnail(size)

            thumb_io = BytesIO()
            img.save(thumb_io, "JPEG", quality=85)

            thumbnail = File(thumb_io, name=image.name)

            return thumbnail

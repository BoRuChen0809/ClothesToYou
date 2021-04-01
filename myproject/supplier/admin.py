from django.contrib import admin

# Register your models here.
from .models import Supplier, Product, SKU, Stored

admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(SKU)
admin.site.register(Stored)
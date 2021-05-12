from django.contrib import admin
from .models import Clothes2You_User, Shopping_Car, Order, Order_Detail

# Register your models here.
admin.site.register(Clothes2You_User)
admin.site.register(Shopping_Car)
admin.site.register(Order)
admin.site.register(Order_Detail)
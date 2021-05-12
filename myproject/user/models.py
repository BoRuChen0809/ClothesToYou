from django.db import models

# Create your models here.
from django.db.models import Manager
from supplier.models import Product, SKU, Stored, Supplier

'''
class Clothes2You_User(models):
    name = models.OneToOneField(User.username)
    mail = models.OneToOneField(User.email)
    phone_1 = models.CharField(max_length=12)
    phone_2 = models.CharField(max_length=12)
    pwd = models.OneToOneField(User.password)
    salt = models.IntegerField()
    address = models.CharField(max_length=100)
    active = models.OneToOneField(User.is_active)
'''

class Clothes2You_User(models.Model):
    Mail = models.EmailField(default=None, primary_key=True)
    Name = models.CharField(max_length=50, default=None)
    PWD = models.BinaryField()
    Salt = models.BinaryField()
    Active = models.BooleanField(default=False)
    Phone_1 = models.CharField(max_length=12, default=None)
    #Phone_2 = models.CharField(max_length=12, default="")
    Address = models.CharField(max_length=100, default="")
    GENDER_CHOICES = (('男', 'Male'), ('女', 'Female'), ('不願透漏', 'Null'))
    Gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='N')

class Shopping_Car(models.Model):
    User = models.ForeignKey(Clothes2You_User, on_delete=models.CASCADE, default=None)
    Product = models.ForeignKey(Stored, on_delete=models.CASCADE, default=None)
    Quantity = models.IntegerField(default=None)

class Order(models.Model):
    ID = models.CharField(primary_key=True, max_length=11)
    User = models.ForeignKey(Clothes2You_User, on_delete=models.CASCADE, default=None)
    Supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, default=None)
    STATE_CHOICES = (('準備中', '準備中'), ('已出貨', '已出貨'), ('已到貨', '已到貨'), ('取消', '取消'), ('完成', '完成'))
    State = models.CharField(max_length=10, choices=STATE_CHOICES, default='準備中')
    DateTime = models.DateTimeField(auto_now_add=True)
    Receiver = models.CharField(max_length=50,default=None)
    Mail = models.EmailField(default=None)
    Phone = models.CharField(max_length=12, default=None)
    Address = models.CharField(max_length=100, default=None)
    Total_Price = models.IntegerField(default=None)

class Order_Detail(models.Model):
    ID = models.ForeignKey(Order, on_delete=models.CASCADE, default=None)
    Stored = models.ForeignKey(Stored, on_delete=models.CASCADE, default=None)
    Quantity = models.IntegerField(default=None)


class UserManager(Manager):
    def createUser(mail,name,pwd,salt,phone1):
        user = Clothes2You_User(Name=name,Mail=mail,PWD=pwd,Salt=salt,Phone_1=phone1)
        user.save()
        '''
    def update(self,mail=None, phone1=None, address=None):
        user = Clothes2You_User.objects.filter(Mail=mail)
        self.update_phone(user[0],phone1)
        self.update_address(user[0],address)

    def update_phone(user, phone):
        if phone is not None:
            user.update(Phone_1=phone)
    def update_address(user,address):
        if address is not None:
            user.update(Address=address)
                '''





from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Create your models here.
from django.db.models import Manager

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
    Mail = models.EmailField(default="")
    Name = models.CharField(max_length=50,default="")
    PWD = models.BinaryField()
    Salt = models.BinaryField()
    Active = models.BooleanField(default=False)
    Phone_1 = models.CharField(max_length=12, default="")
    Phone_2 = models.CharField(max_length=12, default="")
    Address = models.CharField(max_length=100, default="")
    GENDER_CHOICES = (('M','Male'),('F','Female'),('N','Null'),)
    Gender = models.CharField(max_length=1,choices=GENDER_CHOICES,default='N')

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





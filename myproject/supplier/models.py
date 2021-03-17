from django.db import models

# Create your models here.

class Supplier(models.Model):
    ID = models.CharField(max_length=8, default=None)           #統編****************
    B_Name = models.CharField(max_length=100,default=None)      #公司名稱****************
    BU_Name = models.CharField(max_length=50,default=None)      #負責人姓名
    Phone = models.CharField(max_length=12, default=None)
    Mail = models.EmailField(default=None)
    PWD = models.BinaryField()
    Salt = models.BinaryField()
    Active = models.BooleanField(default=False)                 #**********************
    Address = models.CharField(max_length=100, default=None)
    Picture = models.ImageField(default=None)
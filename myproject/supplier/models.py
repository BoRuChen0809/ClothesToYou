from django.db import models

# Create your models here.

class Supplier(models.Model):
    S_ID = models.CharField(max_length=8, default=None,primary_key=True)           #統編****************
    C_Name = models.CharField(max_length=100,default=None)      #公司名稱****************
    Principal = models.CharField(max_length=50,default=None)      #負責人姓名
    Phone = models.CharField(max_length=12, default=None)
    Mail = models.EmailField(default=None)
    PWD = models.BinaryField()
    Salt = models.BinaryField()
    Active = models.BooleanField(default=False)                 #**********************
    Address = models.CharField(max_length=100, default=None)
    Picture = models.ImageField(upload_to='brand/',default=None,blank=True)

'''

class Product(models.Model):
    ID = models.CharField(max_length=50,default=None)
    Name = models.CharField(max_length=50,default=None)
    Price = models.IntegerField(max_length=5,default=None)
    Brand = models.ForeignKey(Supplier,default=None,on_delete=models.CASCADE)
    Genre = models.CharField(max_length=10,default=None)
    Category = models.CharField(max_length=10,default=None)
    SAle_Category = models.CharField(max_length=10,default=None)

class SKU_Product(models.Model):
    SKU_ID = models.CharField(max_length=100 ..,default=None)
    Product = models.ForeignKey(Product,defa                           
    ult=None,on_delete=models.CASCADE)
    Size = models.CharField() 
    Picture = models.ImageField()

'''

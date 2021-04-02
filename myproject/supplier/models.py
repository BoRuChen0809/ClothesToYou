from django.db import models

# Create your models here.

class Supplier(models.Model):
    S_ID = models.CharField(max_length=8, default=None,primary_key=True)
    C_Name = models.CharField(max_length=100, default=None)
    Principal = models.CharField(max_length=50, default=None)
    Phone = models.CharField(max_length=12, default=None)
    Mail = models.EmailField(default=None)
    PWD = models.BinaryField()
    Salt = models.BinaryField()
    Active = models.BooleanField(default=False)
    Address = models.CharField(max_length=100, default=None)
    Picture = models.ImageField(upload_to='brand/', default=None, blank=True)
class Product(models.Model):

    ID = models.CharField(max_length=50, default=None)
    Name = models.CharField(max_length=50, default=None)
    Price = models.IntegerField(default=None)
    Brand = models.ForeignKey(Supplier, default=None, on_delete=models.CASCADE)
    GENRE_CHOICES = (("MEN", "男士"), ("WOMEN", "女士"), ("KIDS", "孩童"), ("BABY", "嬰幼兒"), ("Pregnant", "孕婦"))
    Genre = models.CharField(max_length=10, choices=GENRE_CHOICES, default=None)
    CATEGORY_CHOICES = (("top", "上衣類"), ("shirt", "襯衫類"), ("undies", "內衣類"),
                        ("coat", "外套類"), ("pants", "下身類"), ("accessories", "配件類"),
                        ("dress", "洋裝類"), ("sport", "運動類"), ("shoes", "鞋類"))
    Category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=None)
    Sale_Category = models.CharField(max_length=10, default=None)

class SKU(models.Model):
    SKU_ID = models.CharField(max_length=100, default=None)
    Product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    COLOR_CHOICES = (("red", "紅"), ("orange", "橙"), ("yellow", "黃"), ("pink", "粉紅"),
                     ("cyan", "青"), ("blue", "藍"), ("purple", "紫"), ("green", "綠"),
                     ("gray", "灰"), ("black", "黑"), ("white", "白"), ("brown", "咖啡"))
    Color = models.CharField(max_length=8, choices=COLOR_CHOICES, default=None)
    Picture = models.ImageField(upload_to='products/')

class Stored(models.Model):
    sku = models.ForeignKey(SKU,default=None,on_delete=models.CASCADE)
    SIZE_CHOICES = (("XS", "XS"), ("S", "S"), ("M", "M"), ("L", "L"), ("XL", "XL"), ("XXL", "XXL"))
    Size = models.IntegerField(default=None)
    Stored = models.IntegerField(default=None)
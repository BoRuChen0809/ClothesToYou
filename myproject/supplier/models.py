from django.db import models

# Create your models here.

class Supplier(models.Model):
    S_ID = models.CharField(max_length=8, default=None, primary_key=True)
    C_Name = models.CharField(max_length=100, default=None)
    Principal = models.CharField(max_length=50, default=None)
    Phone = models.CharField(max_length=12, default=None)
    Mail = models.EmailField(default=None)
    PWD = models.BinaryField()
    Salt = models.BinaryField()
    Active = models.BooleanField(default=False)
    Address = models.CharField(max_length=100, default=None)
    Picture = models.ImageField(upload_to='brand/', default=None, blank=True)

    def __str__(self):
        return self.C_Name

class Product(models.Model):
    ID = models.CharField(max_length=20, default=None, primary_key=True)
    Name = models.CharField(max_length=50, default=None)
    Price = models.IntegerField(default=None)
    Brand = models.ForeignKey(Supplier, default=None, on_delete=models.CASCADE)
    GENRE_CHOICES = (("男士", "男士"), ("女士", "女士"), ("孩童", "孩童"), ("嬰幼兒", "嬰幼兒"), ("孕婦", "孕婦"))
    Genre = models.CharField(max_length=10, choices=GENRE_CHOICES, default=None)
    CATEGORY_CHOICES = (("上衣類", "上衣類"), ("襯衫類", "襯衫類"), ("內衣類", "內衣類"),
                        ("外套類", "外套類"), ("下身類", "下身類"), ("配件類", "配件類"),
                        ("洋裝類", "洋裝類"), ("運動類", "運動類"), ("鞋類", "鞋類"))
    Category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default=None)
    Sale_Category = models.CharField(max_length=10, default=None)
    Description = models.CharField(max_length=255, default=None)

    def __str__(self):
        return self.Genre + self.Category + ":" +self.Name

def product_pic_url(instance, filename):
    return 'products/{0}/{1}/{2}/{3}'.format(instance.Product.Genre, instance.Product.Category, instance.Product.ID,filename)

class SKU(models.Model):
    SKU_ID = models.CharField(max_length=25, default=None, primary_key=True)
    Product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    COLOR_CHOICES = (("red", "紅"), ("orange", "橙"), ("yellow", "黃"), ("pink", "粉紅"),
                     ("cyan", "青"), ("blue", "藍"), ("purple", "紫"), ("green", "綠"),
                     ("gray", "灰"), ("black", "黑"), ("white", "白"), ("brown", "咖啡"))
    Color = models.CharField(max_length=100, choices=COLOR_CHOICES, default=None)
    Picture = models.ImageField(upload_to=product_pic_url)

    def __str__(self):
        return self.Color + "_" + self.Product.Name

class Stored(models.Model):
    sku = models.ForeignKey(SKU,default=None, on_delete=models.CASCADE)
    SIZE_CHOICES = (("XS", "XS"), ("S", "S"), ("M", "M"), ("L", "L"), ("XL", "XL"), ("XXL", "XXL"))
    Size = models.CharField(max_length=8, choices=SIZE_CHOICES, default=None)
    stored = models.IntegerField(default=None)

    def __str__(self):
        return self.Size + "_" + self.sku.Color + "_" + self.sku.Product.Name
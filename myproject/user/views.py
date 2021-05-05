
import re,bcrypt

from PIL import Image
from django.contrib.postgres.search import SearchVector
from django.template import loader
from .models import Clothes2You_User, UserManager, Shopping_Car
from supplier.models import Product, SKU, Stored, Supplier
from django.shortcuts import render, redirect
from django.core import serializers
from django.contrib.postgres import search
# Create your views here.


# **************************** views ***************************** #

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.POST:
        warning_list = []
        #姓名不得為空值或""
        name = request.POST['user_name']
        if check_name(name):
            warning_list.append("姓名有誤")
        #信箱格式檢查
        email = request.POST['user_email']
        if check_email(email):
            warning_list.append("電子郵件格式有誤")
        #信箱存在?
        if check_existmail(email):
            warning_list.append("此電子郵件已存在")
        #密碼格式檢查
        pwd = request.POST['user_password']
        if check_password(pwd):
            warning_list.append("密碼格式不符")
        #確認密碼
        check_pwd = request.POST['password_check']
        if check_pwd_match(pwd, check_pwd):
            warning_list.append("密碼與確認密碼不符")

        #電話格式
        phone = request.POST['user_phone']
        if check_phone(phone):
            warning_list.append("電話話碼格式有誤")

        if len(warning_list) > 0:
            context = {'warning': warning_list}
            return render(request, 'user_register.html', context)
        else:
            salt,pwd = hashpwd(pwd)
            UserManager.createUser(email,name,pwd,salt,phone)
            #member = Clothes2You_User(Name=name,Mail=email,PWD=pwd,Salt=salt,Phone_1=phone)
            #member.save()
            context = {'identification': 'user'}
            return render(request, 'register_succeed.html', context)
    else:
        return render(request, 'user_register.html')

def login(request):
    if request.POST:
        try:
            email = request.POST['user_email']
            pwd = request.POST['user_password']

            user = Clothes2You_User.objects.get(Mail=email)

            if bcrypt.checkpw(bytes(pwd, 'utf-8'), bytes(user.PWD)):
                request.session['user_mail'] = user.Mail
                return redirect('profile')
            else:
                # print("登入失敗")
                context = {'failed': "帳號或密碼錯誤"}
                return render(request, 'user_login.html', context)
        except:
            context = {'failed': "帳號或密碼錯誤"}
            return render(request, 'user_login.html', context)
    elif 'user_mail' in request.session:
        return redirect('profile')


    return render(request, 'user_login.html')

def logout(request):
    del request.session['user_mail']
    return redirect('index')

def profile(request):
    if 'user_mail' not in request.session:
        return redirect('login')
    mail = request.session['user_mail']
    user = Clothes2You_User.objects.get(Mail=mail)

    context = {'user':user,'genrer_tuple':Clothes2You_User.GENDER_CHOICES}
    return render(request, 'user_profile.html',context)

def changeprofile(request):
    if 'user_mail' not in request.session:
        return redirect('login')
    if request.POST:
        phone = request.POST['user_phone']
        if check_phone(phone):
            context = {'warn_1':"電話話碼格式有誤"}
            return render(request,'user_profile.html',context)
        gender = request.POST['radio']
        #print(gender)
        address = request.POST['user_address']



        mail = request.session['user_mail']
        user = Clothes2You_User.objects.get(Mail=mail)

        user.Phone_1 = phone
        user.Gender = gender
        user.Address = address
        user.save()

        return redirect('profile')

    return redirect('profile')

def changepwd(request):
    if request.POST:
        old = request.POST['user_password']
        new = request.POST['new_user_password']
        check_new = request.POST['new_password_check']

        mail = request.session['user_mail']

        user = Clothes2You_User.objects.get(Mail=mail)

        if bcrypt.checkpw(bytes(old, 'utf-8'), bytes(user.PWD))\
                and (not check_password(new))\
                and (not check_pwd_match(new,check_new)) :
            new_salt,new_hashed = hashpwd(new)
            user.Salt = new_salt
            user.PWD = new_hashed
            user.save()

            return redirect('logout')
        else:
            warning_list = []
            # 密碼格式檢查
            if check_password(old):
                warning_list.append("密碼格式不符")
            if check_pwd_match(new, check_new):
                warning_list.append("密碼與確認密碼不符")
            if not bcrypt.checkpw(bytes(old, 'utf-8'),bytes(user.PWD)):
                warning_list.append("舊密碼輸入錯誤")
            context = {'warn_2':warning_list, 'user':user}
            return render(request, 'user_profile.html',context)

    return redirect('profile')

def resetpwd(request):
    return redirect('profile')

def hashpwd(pwd):
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(pwd.encode('utf-8'), salt)
    return salt,hashed_pwd

def orders(request):
    return render(request, 'user_orders.html')

def product_detail(request, product_ID):
    product = Product.objects.get(ID = product_ID)
    skus = SKU.objects.filter(Product = product)
    sizes = []
    for sku in skus:
        S = Stored.objects.filter(sku=sku)
        for s in S:
            if s.Size not in sizes:
                sizes.append(s.Size)
    context = {'product': product, 'skus': skus, 'sizes': sizes}
    if request.POST:
        if 'user_mail' not in request.session:
            return redirect('login')
        else:
            mail = request.session['user_mail']
            user = Clothes2You_User.objects.get(Mail=mail)
            sku_id = request.POST['color']
            sku = SKU.objects.get(SKU_ID=sku_id)
            size = request.POST['size']
            store = Stored.objects.filter(sku=sku).get(Size=size)
            quantity = int(request.POST['quantity'])

            if "add" in request.POST:
                items = Shopping_Car.objects.filter(User=user)
                can_add = True
                for item in items:
                    if item.Product.sku == store.sku:
                        can_add = False

                if can_add:
                    new_item = Shopping_Car(User=user, Product=store, Quantity=quantity)
                    new_item.save()
                    print("加入購物車")

            elif "buy" in request.POST:
                print("直接購買")

    return render(request, 'user_product.html', context)




def search(request):
    if 'image' in request.FILES:
        image = request.FILES['image']
        print(type(image))
        pic = Image.open(image)

    elif 'search' in request.POST:
        Text = request.POST['search']



    else:
        return redirect('index')
    return redirect('index')

def mycart(request):
    if 'user_mail' not in request.session:
        return redirect('login')
    else:
        mail = request.session['user_mail']
        user = Clothes2You_User.objects.get(Mail=mail)
        shopping_items = Shopping_Car.objects.filter(User=user)
        items=[]
        for item in shopping_items:
            item = temp_product(item)
            items.append(item)

        context = {'items': items}
        return render(request, 'user_shopcart.html', context)

class temp_product():
    #一次放入單個stored
    def __init__(self, item):
        self.item = item
        self.Stored = item.Product
        self.SKU = self.Stored.sku
        self.Product = self.SKU.Product
        self.Quantity = item.Quantity
        self.sizes = []
        self.setSizes(self.SKU)
        self.skus = []
        self.setSKUs(self.Product)

    def setSizes(self,sku):
        S = Stored.objects.filter(sku=sku)
        for s in S:
            if s.Size not in self.sizes:
                self.sizes.append(s.Size)

    def setSKUs(self,product):
        SKUs = SKU.objects.filter(Product=product)
        for sku in SKUs:
            self.skus.append(sku)










def searchlist(request):
    products = Product.objects.all()
    context = {'products':products}

    return render(request, 'user_search.html', context)





#有問題rerturn True
def check_name(str):
    if str == "":
        return True
    return False
def check_email(str):
    mail = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return not mail.match(str)
def check_existmail(str):
    try:
        if len(Clothes2You_User.objects.filter(Mail=str))>0:
            return True
        else: return False
    except:
        return False
def check_password(str):
    eight_char = False
    has_Num = False
    has_Char = False
    for c in str:
        if c.isnumeric():
            has_Num = True
            break

    for c in str:
        if c.isalpha():
            has_Char = True
            break

    if len(str) >= 8:
        eight_char = True

    return not(eight_char and has_Char and has_Num)
def check_pwd_match(pwd, c_pwd):
    if pwd != c_pwd:
        return True
    return False
def check_phone(str):
    phone = re.compile(r"^09+\d{8}")
    return not phone.match(str)








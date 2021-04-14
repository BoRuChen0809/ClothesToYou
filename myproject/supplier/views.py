import re

import bcrypt
from django.shortcuts import render, redirect

# Create your views here.
from .models import Supplier, Product, SKU, Stored


# *********************** views ******************************** #
def sindex(request):
    return render(request, 'supplier_index.html')

def become_partner(request):
    if request.POST:
        warning_list = []

        id = request.POST['company_id']
        if check_id(id) or check_exist(id):
            warning_list.append("統編有誤")
            print(check_id(id))
            print(check_exist(id))

        c_name = request.POST['company_name']  # 公司名稱****************
        if check_name(c_name):
            warning_list.append("公司名稱有誤")

        principal = request.POST['supplier_name']  # 負責人姓名
        if check_name(principal):
            warning_list.append("姓名有誤")

        phone = request.POST['supplier_phone']
        if check_phone(phone):
            warning_list.append("電話號碼有誤")

        mail = request.POST['supplier_email']
        if check_email(mail):
            warning_list.append("電子郵件有誤")

        pwd = request.POST['supplier_password']
        if check_password(pwd):
            warning_list.append("密碼有誤")

        check_pwd = request.POST['password_check']
        if check_pwd_match(pwd,check_pwd):
            warning_list.append("確認密碼有誤")

        address = request.POST['company_address']
        if check_name(address):
            warning_list.append("通訊地有誤")
        #Picture = request.POST['']

        if len(warning_list) > 0:
            context = {'warning': warning_list}
            return render(request, 'supplier_become_partner.html', context)
        else:
            salt,pwd = hashpwd(pwd)
            supplier = Supplier(S_ID=id,C_Name=c_name,Principal=principal,Phone=phone,Mail=mail,PWD=pwd,Salt=salt,Active=False,Address=address)
            supplier.save()
            #return render(request, 'register_succeed.html')
            context = {'identification': 'supplier'}
            return render(request, 'register_succeed.html', context)
    return render(request, 'supplier_become_partner.html')

def slogin(request):
    if request.POST:
        try:
            c_name = request.POST['company_name']
            c_id = request.POST['company_id']
            pwd = request.POST['supplier_password']

            supplier = Supplier.objects.get(S_ID=c_id)

            if bcrypt.checkpw(bytes(pwd, 'utf-8'), bytes(supplier.PWD)) and supplier.C_Name == c_name:
                request.session['supplier_id'] = supplier.S_ID
                return redirect('sprofile')
            else:
                context = {'failed': "登入資訊或密碼錯誤"}
                return render(request, 'supplier_login.html', context)
        except:
            context = {'failed': "登入資訊或密碼錯誤"}
            return render(request, 'supplier_login.html', context)
    elif 'supplier_id' in request.session:
        return redirect('sprofile')

    return render(request, 'supplier_login.html')

def slogout(request):
    del request.session['supplier_id']
    return redirect('sindex')

def sprofile(request):
    if 'supplier_id' not in request.session:
        return redirect('slogin')
    c_id = request.session['supplier_id']
    supplier = Supplier.objects.get(S_ID=c_id)
    products = Product.objects.filter(Brand=supplier)
    context = {'supplier':supplier, 'products':products}
    return render(request, 'supplier_profile.html',context)

def changesprofile(request):
    if request.POST:
        warning_list = {}

        principal = request.POST['supplier_name']
        if check_name(principal):
            warning_list.append("姓名有誤")

        phone = request.POST['supplier_phone']
        if check_phone(phone):
            warning_list.append("電話號碼有誤")

        mail = request.POST['supplier_email']
        if check_email(mail):
            warning_list.append("電子郵件有誤")

        address = request.POST['company_address']
        if check_name(address):
            warning_list.append("通訊地有誤")



        c_id = request.session['supplier_id']
        supplier = Supplier.objects.get(S_ID=c_id)

        if len(warning_list) > 0:
            context = {'warn1':warning_list}
            return render(request, 'supplier_profile.html',context)
        else:
            supplier.Principal = principal
            supplier.Mail = mail
            supplier.Address =address
            supplier.Phone = phone
            print("成功!!!")
            return redirect('sprofile')
    return redirect('sprofile')

def profileimg(request):
    if request.POST:
        c_id = request.session['supplier_id']
        supplier = Supplier.objects.get(S_ID=c_id)
        if 'image' in (request.FILES):
            img = request.FILES['image']
            filename = supplier.S_ID + '.' + splitext(img.name)
            img.name = filename
            supplier.Picture = img
            supplier.save()
            return redirect('sprofile')

    elif 'supplier_id' not in request.session:
        return redirect('slogin')
    return redirect('sprofile')

def changespwd(request):
    if request.POST:
        old = request.POST['supplier_password']
        new = request.POST['new_supplier_password']
        check_new = request.POST['new_password_check']

        c_id = request.session['supplier_id']

        supplier = Supplier.objects.get(S_ID=c_id)

        if bcrypt.checkpw(bytes(old, 'utf-8'), bytes(supplier.PWD))\
                and (not check_password(new))\
                and (not check_pwd_match(new,check_new)) :
            new_salt,new_hashed = hashpwd(new)
            supplier.Salt = new_salt
            supplier.PWD = new_hashed
            supplier.save()
            print('修改成功')
            return redirect('slogout')
        else:
            warning_list = []
            # 密碼格式檢查
            if check_password(old):
                warning_list.append("密碼格式不符")
            if check_pwd_match(new, check_new):
                warning_list.append("密碼與確認密碼不符")
            if not bcrypt.checkpw(bytes(old, 'utf-8'),bytes(supplier.PWD)):
                warning_list.append("舊密碼輸入錯誤")
            context = {'warn_2':warning_list, 'supplier':supplier}
            return render(request, 'supplier_profile.html',context)
    elif 'supplier_id' not in request.session:
        return redirect('slogin')
    return redirect('sprofile')

colors_id = {"red":"01", "orange":"02", "yellow":"03", "pink":"04",
          "cyan":"05", "blue":"06", "purple":"07", "green":"08",
          "gray":"09", "black":"10", "white":"11", "brown":"12"}

def addproduct(request):
    if request.POST:
        c_id = request.session['supplier_id']
        supplier = Supplier.objects.get(S_ID=c_id)

        product_id = c_id + create_product_id(supplier)
        product_name = request.POST['product_name']
        product_price = request.POST['product_price']
        genre = request.POST['genre']
        category = request.POST['category']
        sales_category = request.POST['product_sales_category']
        sizes = request.POST.getlist('size')
        product_description = request.POST['product_description']

        product = Product(ID=product_id, Name=product_name, Brand=supplier, Price=int(product_price),
                          Genre=genre, Category=category, Sale_Category=sales_category, Description=product_description)
        product.save()

        color = request.POST.getlist('color')
        for c in color:
            sku_id = product_id + colors_id[c]
            str = 'image'+c
            img = request.FILES[str]
            filename = sku_id + '.' + splitext(img.name)
            img.name = filename
            Sku = SKU(SKU_ID=sku_id, Product=product, Color=c, Picture=img)
            Sku.save()
            for s in sizes:
                size_stored = Sku.Color + "_" + s +"_stored"
                print(size_stored)
                stored = request.POST[size_stored]
                print(stored)
                Store = Stored(sku=Sku, Size=s, stored=stored)
                Store.save()

        genre_choices = Product.GENRE_CHOICES
        category_choices = Product.CATEGORY_CHOICES
        color_chioces = SKU.COLOR_CHOICES
        size_choices = Stored.SIZE_CHOICES
        context = {'genre': genre_choices, 'category': category_choices, 'color': color_chioces, 'size': size_choices}


        return render(request, 'supplier_addproduct.html',context)

    genre_choices = Product.GENRE_CHOICES
    category_choices = Product.CATEGORY_CHOICES
    color_chioces = SKU.COLOR_CHOICES
    size_choices = Stored.SIZE_CHOICES
    context = {'genre':genre_choices, 'category':category_choices, 'color':color_chioces, 'size':size_choices}
    return render(request, 'supplier_addproduct.html',context)

def editproduct(request, product_ID):
    if request.POST:
        product = Product.objects.get(ID=product_ID)
        product.Name = request.POST['product_name']
        product.Price = int(request.POST['product_price'])
        product.Genre = request.POST['genre']
        product.Category = request.POST['category']
        product.Sale_Category = request.POST['product_sales_category']
        product.Description = request.POST['product_description']
        product.save()
        color = request.POST.getlist('color')
        sizes = request.POST.getlist('size')

        sku = SKU.objects.filter(Product=product)

        for c in color:
            sku_id = product.ID + colors_id[c]
            str = 'image' + c
            if str in request.FILES:
                img = request.FILES[str]
                filename = sku_id + '.' + splitext(img.name)
                img.name = filename
            else:
                img = None

            try:
                old = sku.get(SKU_ID=sku_id)
                if img is not None:
                    old.Picture = img
                    old.save()
            except:
                new = SKU(SKU_ID=sku_id, Product=product, Color=c, Picture=img)
                new.save()
                for s in sizes:
                    stored = Stored(sku=new, Size=s, stored=0)
                    stored.save()
            sku = sku.exclude(SKU_ID=sku_id)
        sku.delete()

        sku = SKU.objects.filter(Product=product)
        for Sku in sku:
            print(Sku)
            stored = Stored.objects.filter(sku=Sku)
            for size in sizes:
                num_id = Sku.Color + "_" + size + "_stored"
                num = request.POST[num_id]
                try:
                    s = stored.get(Size=size)
                    s.stored = num
                    print("存在")
                except:
                    s = Stored(sku=Sku, Size=size, stored=num)
                    print("不存在")
                print(s)
                s.save()
        return redirect('sprofile')


    product = Product.objects.get(ID=product_ID)
    skus = SKU.objects.filter(Product=product)
    stored = Stored.objects.filter(sku=skus[0])

    size_selected = []
    for s in stored:
        size_selected.append(s.Size)

    color_selected = []
    for c in skus:
        color_selected.append(c.Color)

    stored_list = []
    for sku in skus:
        stored_list.append(Stored.objects.filter(sku=sku))




    genre_choices = Product.GENRE_CHOICES
    category_choices = Product.CATEGORY_CHOICES
    color_choices = SKU.COLOR_CHOICES
    size_choices = Stored.SIZE_CHOICES

    context = {'product': product,  'size_selected': size_selected, 'genre': genre_choices,
               'category': category_choices, 'color': color_choices, 'size': size_choices,
               'color_selected': color_selected, 'sku': skus, 'stored':stored_list}
    return render(request, 'supplier_editproduct.html', context)

# ************************* Functions ***************************** #
def splitext(file):
    filename = file.split('.')
    return filename[-1]
def create_product_id(supplier):
    try:
        num = len(Product.objects.filter(Brand=Supplier))
        num += 1
        if 9999 > num >= 1000:
            return str(num)
        elif 1000 > num >= 100:
            return '0'+str(num)
        elif 100 > num >= 10:
            return '00'+str(num)
        else:
            return '000'+str(num)
    except:
        return '0001'
def hashpwd(pwd):
    salt = bcrypt.gensalt()
    hashed_pwd = bcrypt.hashpw(pwd.encode('utf-8'), salt)
    return salt,hashed_pwd

#有問題rerturn True
def check_id(str):
    list = [1, 2, 1, 2, 1, 2, 4, 1]
    serial_list = []
    new_list = []

    for c in str:
        serial_list.append(int(c))
        if not c.isnumeric():
            return True
            break

    if len(serial_list) != 8:
        return True

    for i in range(8):
        temp = serial_list[i] * list[i]
        new_list.append(int(temp / 10) + int(temp % 10))

    s = sum(new_list)
    if s % 10 != 0 or (serial_list[6] == 7 and (s - new_list[6] % 10 == 0 or s - new_list[6] % 10 == 9)):
        return True

    return False
def check_name(str):
    if str == "":
        return True
    return False
def check_email(str):
    mail = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return not mail.match(str)
def check_exist(str):
    try:
        if len(Supplier.objects.filter(S_ID=str)) > 0:
            return True
        else:
            return False
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


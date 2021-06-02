
import re,bcrypt

from PIL import Image
from django.contrib.postgres.search import SearchVector
from django.template import loader
from .models import Clothes2You_User, UserManager, Shopping_Car, Order, Order_Detail
from supplier.models import Product, SKU, Stored, Supplier
from django.shortcuts import render, redirect
from django.core import serializers
from django.contrib.postgres import search
from datetime import datetime as dt
from datetime import timedelta as delay
# Create your views here.
import os
from user.modules.image_search.image_search import ReverseImageSearch
from user.modules.get_current_time import get_current_time
from supplier.models import Product
from user.recommender import Recommender

# **************************** views ***************************** #

def index(request):
	"""
	# origin:
    return render(request, 'index.html')
	"""
	
	# 6/2:
	#return render(request, 'index.html')
    #'''
    products = Product.objects.all()
    #sku_list = [prod.sku_set.first() for prod in Product.objects.all()]
    skus = [prod.sku_set.first() for prod in products]
    #context = {'products': products, 'skus': skus}
    items = list()
    for prod in products:
        curr_item = dict()
        curr_item["Name"] = prod.Name
        curr_item["Price"] = prod.Price
        curr_item["sku"] = prod.sku_set.first()
        curr_item["product"] = prod
        items.append(curr_item)
    #context = {'products': products}
    context = {'items': items}
    return render(request, 'index.html', context)

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
    
	# get recommendations related to current product (Item-based)
    r = Recommender()
    recommendations = r.get_recommendations(product_ID, 4)
    context["recommendations"] = recommendations
	
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
    # image search
    if "image" in request.FILES:
        ''' 1. 將當前上傳圖片放到 ./media/search_images '''
        image = request.FILES['image']
        print(type(image))
        #<class 'django.core.files.uploadedfile.InMemoryUploadedFile'>
        
        upload_img = Image.open(image)
        #upload_img.show()
        input_img_dir = "./media/search_images"
        if not os.path.exists(input_img_dir):
            os.mkdir(input_img_dir)
        current_time = get_current_time()
        upload_img_path = os.path.abspath(f"{input_img_dir}/{current_time}.jpg")
        upload_img.save(upload_img_path)
        print(f"上傳圖片已保存到: {upload_img_path}")
        
        method = "v2"  # method | choices: ("v0","v1","v2")
        MAX_AMT = N = 100  # MAX_AMT must >= 30 | suggestion: 100
        top_K = K = 50  # top_K must >= 10 | E.g., 20, 100, ...
        #raw_img = "D:/MyPrograms/Clothes2U/DB/訓練圖片 DB/origin/dataset/test_data_to_classify/2/GU_咖啡色_洋裝類.jpg"
        
        ''' 2. 對當前上傳圖片，用 模擬(=>不是上架商品)的圖片DB 進行圖片搜尋 '''
        simulative_img_db_path = "C:/Users/user/Desktop/ClothesToYou-v3/myproject/media/img_db_3"
        ris = ReverseImageSearch(method, MAX_AMT, top_K, upload_img_path, simulative_img_db_path)
        similar_image_paths = ris.exec_reverse_image_search()
        similar_image_paths = [f"/{'/'.join(path_.split('/')[6:])}" for path_ in similar_image_paths]
        print("Top similar images:", *(path_ for path_ in similar_image_paths), sep='\n', end='\n'*2)

        return render(request,
                      'user_search.html',
                      {"img_paths": similar_image_paths})
    
    # text search
    elif "search" in request.POST:
        text = request.POST['search']
        print(f"親愛的用戶，您剛剛搜尋的字詞為：\"{text}\"")
        yy, MM, dd, HH, mm, ss = get_current_time().split('_')
        print(f"今天是: {yy}年 {MM}月 {dd}日")
        print(f"現在時間是: {HH}點 {mm}分 {ss}秒")
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

def remove_from_cart(request, item_ID):
    if 'user_mail' not in request.session:
        return redirect('login')
    else:
        item = Shopping_Car.objects.get(id = item_ID)
        item.delete()
        return redirect('mycart')

def checkout(request):
    if 'user_mail' not in request.session:
        return redirect('login')
    elif request.POST:
        print(request.POST)
        wantbuy_list = request.POST.getlist("want2buy")
        wantbuy_list = list(map(int,wantbuy_list))
    
        if len(wantbuy_list)<=0:
            return redirect('mycart')

        supplier_set = set()
        for index in wantbuy_list:
            quantity_index = 'quantity_' + str(index)
            quantity = int(request.POST[quantity_index])
            item = Shopping_Car.objects.get(id=index)
            supplier_set.add(item.Product.sku.Product.Brand)
            item.Quantity = quantity
            item.save()

        if 'save' in request.POST:
            return redirect('mycart')
        elif 'checkout' in request.POST:
            mail = request.session['user_mail']
            user = Clothes2You_User.objects.get(Mail=mail)
            items = Shopping_Car.objects.filter(User=user)
            
            for item in items:
                if item.id in wantbuy_list:
                    item.Selected = True
                else:
                    item.Selected = False
                item.save()

            context = {'user': user}
            # Using Item2Item Recommender: 
            # The recorded number of purchased products 
            # need to be increased by 1 (in the co-occurence matrix)
            r = Recommender()
            
            tmp_stored_list = [item.Product for item in items]
            print("tmp_stored_list", tmp_stored_list, '\n')
            
            tmp_sku_list = [sorted_obj.sku for sorted_obj in tmp_stored_list]
            print("tmp_sku_list", tmp_sku_list, '\n')
            
            purchased_products = [sku_obj.Product for sku_obj in tmp_sku_list]
            print("purchased_products", purchased_products, '\n')
            
            # it (param of func: `products_bought`) needs Products 
            # i.e., 
            # Shopping_Car(user) => Stored(supplier) => SKU(supplier) => Product(supplier)
            
            purchased_products_IDs = [product.ID for product in purchased_products]
            print("purchased_products_IDs", purchased_products_IDs, '\n')
            r.products_bought(purchased_products_IDs)
            return render(request, 'user_orders.html', context)

    return redirect('mycart')

def searchlist(request):
    products = Product.objects.all()
    context = {'products':products}
. 
    return render(request, 'user_search.html', context)

'''
def orderdetails(request):
    if request.POST:
        supplier_set = set()
        mail = request.session['user_mail']
        user = Clothes2You_User.objects.get(Mail=mail)
        items = Shopping_Car.objects.filter(User=user).filter(Selected=True)

        r_name = request.POST['receiver_name']
        r_phone = request.POST['receiver_phone']
        r_email = request.POST['receiver_email']
        r_address = request.POST['receiver_address']
        datetime = dt.now()
        order_date = datetime.strftime("%y%m%d")

        for item in items:
            supplier_set.add(item.Product.sku.Product.Brand)

        show_orders = []
        total = 0
        for s in supplier_set:
            Orders = Order.objects.filter(DateTime__date=dt.today())
            num = len(Orders) + 1
            number = '{0:08d}'.format(num)
            order_id = order_date + number
            order = Order(ID=order_id, User=user, Supplier=s, State='準備中', Receiver=r_name, Mail=r_email, Phone=r_phone, Address=r_address, Total_Price=0)
            order.save()
            total_price = 0
            for item in items:
                if item.Product.sku.Product.Brand == s:
                    price = item.Quantity * item.Product.sku.Product.Price
                    detail = Order_Detail(ID=order, Stored=item.Product, Quantity=item.Quantity, Price=price)
                    detail.save()
                    total_price += price
            order.Total_Price = total_price
            total += total_price
            order.save()
            show_orders.append(temp_order(order))
        items.delete()
        context = {'user': user, 'orders': show_orders, 'total_price': total}
        return render(request, 'user_order_details.html',context)
def searchlist(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'user_search.html', context)

def orderspage(request):
    mail = request.session['user_mail']
    user = Clothes2You_User.objects.get(Mail=mail)
    orders = Order.objects.filter(User=user)
    context = {'orders': orders}

    return render(request, 'user_orders_page.html', context)

def orderdetail(request, order_ID):
    mail = request.session['user_mail']
    user = Clothes2You_User.objects.get(Mail=mail)
    order = Order.objects.get(ID=order_ID)
    details = Order_Detail.objects.filter(ID=order)
    context = {'user': user, 'order': order, 'details': details}
    return render(request, 'user_order_trace.html', context)

def cancelorder(request, order_ID):
    date = dt.now().date()
    days7 = delay(days=8)
    date = date + days7
    order = Order.objects.get(ID=order_ID)
    print(date)
    print(order.DateTime.date())
    num = (date - order.DateTime.date()).days
    if (num <= 7) and (num>=0) :
        order.State = '取消'
        order.save()
        return redirect('orderspage')
    else:
        return redirect('reason', order_ID=order_ID)


def cancelreason(request, order_ID):
    order = Order.objects.get(ID=order_ID)
    if request.POST:
        cancel_description = request.POST['cancel_description']
        print(cancel_description)
        order.State = "申請取消中"
        order.Remark = cancel_description
        order.save()
        return redirect('orderspage')

    context = {'order': order}
    return render(request, 'user_cancel_order.html', context)

'''

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








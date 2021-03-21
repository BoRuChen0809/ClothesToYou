import re

import bcrypt
from django.shortcuts import render, redirect

# Create your views here.
from .models import Supplier


def s_index(request):
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

            return render(request, 'register_succeed.html')


        return render(request, 'register_succeed.html')
    return render(request, 'supplier_become_partner.html')

def slogin(request):
    if request.POST:

        c_name = request.POST['company_name']
        c_id = request.POST['company_id']
        pwd = request.POST['supplier_password']

        print(c_name)
        print(c_id)
        print(pwd)

        supplier = Supplier.objects.get(S_ID = c_id)
        print(supplier)

        if bcrypt.checkpw(bytes(pwd, 'utf-8'), supplier.PWD) and supplier.C_Name==c_name :
            request.session['supplier_id'] = supplier.S_ID
            print("登入成功")
            return redirect('sprofile')
        else:
            print("登入失敗")
            context = {'failed': "登入資訊或密碼錯誤"}
            return render(request, 'supplier_login.html', context)

    elif 'supplier_id' in request.session:
        return redirect('sprofile')

    return render(request, 'supplier_login.html')

def sprofile(request):
    c_id = request.session['supplier_id']
    supplier = Supplier.objects.get(S_ID=c_id)
    context = {'supplier':supplier}
    return render(request, 'supplier_profile.html',context)

def changesprofile(request):
    
    return redirect('sprofile')

def changespwd(request):
    if request.POST:
        old = request.POST['supplier_password']
        new = request.POST['new_supplier_password']
        check_new = request.POST['new_password_check']

        c_id = request.session['supplier_id']

        supplier = Supplier.objects.get(S_ID=c_id)

        if bcrypt.checkpw(bytes(old, 'utf-8'), supplier.PWD)\
                and (not check_password(new))\
                and (not check_pwd_match(new,check_new)) :
            new_salt,new_hashed = hashpwd(new)
            supplier.Salt = new_salt
            supplier.PWD = new_hashed
            supplier.save()

            return redirect('logout')
        else:
            warning_list = []
            # 密碼格式檢查
            if check_password(old):
                warning_list.append("密碼格式不符")
            if check_pwd_match(new, check_new):
                warning_list.append("密碼與確認密碼不符")
            if not bcrypt.checkpw(bytes(old, 'utf-8'),supplier.PWD):
                warning_list.append("舊密碼輸入錯誤")
            context = {'warn_2':warning_list, 'user':supplier}
            return render(request, 'user_profile.html',context)
    return redirect('sprofile')

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
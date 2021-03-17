import base64
import hashlib
import re,bcrypt
from django.template import loader

from django.shortcuts import render, redirect

# Create your views here.
from .models import Clothes2You_User, UserManager


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
            return render(request, 'register_succeed.html')
    else:
        return render(request, 'user_register.html')

def login(request):
    if request.POST:
        email = request.POST['user_email']
        pwd = request.POST['user_password']
        #user = Clothes2You_User.objects.filter(Mail=email)
        user = Clothes2You_User.objects.get(Mail=email)
        '''
               if bcrypt.checkpw(bytes(pwd, 'utf-8'), user[0].PWD):
                   request.session['user_name'] = user[0].Name
                   request.session['user_mail'] = user[0].Mail
                   #print(request.session['user']+"登入成功")
                   #context = {'user':request.session['user_name']}
                   #return render(request, 'user_profile.html',context)
                   return redirect('profile')
               '''
        if bcrypt.checkpw(bytes(pwd, 'utf-8'), user.PWD):
            request.session['user_name'] = user.Name
            request.session['user_mail'] = user.Mail
            #print(request.session['user']+"登入成功")
            #context = {'user':request.session['user_name']}
            #return render(request, 'user_profile.html',context)
            return redirect('profile')

        else:
            #print("登入失敗")
            context = {'failed':"帳號或密碼錯誤"}
            return render(request, 'user_login.html', context)
    elif 'user_mail' in request.session:
        return redirect('profile')


    return render(request, 'user_login.html')

def logout(request):
    request.session.clear()
    return redirect('index')

def profile(request):
    user = Clothes2You_User.objects.get(Mail=request.session['user_mail'])
    context = {'user':user}
    return render(request, 'user_profile.html',context)

def changeprofile(request):
    if request.POST:
        phone = request.POST['user_phone']
        if check_phone(phone):
            context = {'warn_1':"電話話碼格式有誤"}
            return render(request,'user_profile.html',context)
        gender = request.POST['radio']
        address = request.POST['user_address']
        print(gender)


        mail = request.session['user_mail']
        user = Clothes2You_User.objects.get(Mail=mail)
        user.Phone_1 = phone
        user.Address = address

        user.save()

        return  redirect('profile')

    return redirect('profile')

def changepwd(request):
    if request.POST:
        old = request.POST['user_password']
        new = request.POST['new_user_password']
        check_new = request.POST['new_password_check']

        email = request.session['user_mail']
        user = Clothes2You_User.objects.get(Mail=email)

        print(bcrypt.checkpw(bytes(old, 'utf-8'),user.PWD))
        print(check_password(new))
        print(check_pwd_match(new,check_new))

        if bcrypt.checkpw(bytes(old, 'utf-8'), user.PWD) and (not check_password(new)) and (not check_pwd_match(new,check_new)) :
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
            if not bcrypt.checkpw(bytes(old, 'utf-8'),user.PWD):
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

def check_name(str):
    if str == "":
        return True
    return False
def check_email(str):
    mail = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return not mail.match(str)
def check_existmail(str):
    try:
        if len(Clothes2You_User.objects.filter(Name=str))>0:
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

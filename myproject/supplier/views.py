import re

from django.shortcuts import render

# Create your views here.
from .models import Supplier


def s_index(request):
    return render(request, 'supplier_index.html')

def become_partner(request):
    if request.POTS:
        warn_list = []
        id = request.POTS['company_id']
        c_name = request.POTS['company_name']  # 公司名稱****************

        principal = request.POTS['supplier_name']  # 負責人姓名
        phone = request.POTS['supplier_phone']
        mail = request.POTS['supplier_email']
        pwd = request.POTS['supplier_password']
        check_pwd = request.POTS['password_check']
        address = request.POTS['company_address']
        #Picture = request.POTS['']
        return render(request, 'register_succeed.html')
    return render(request, 'supplier_become_partner.html')

def slogin(request):
    return render(request, 'supplier_login.html')

def sprofile(request):
    return render(request, 'supplier_profile.html')




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
        if len(Supplier.objects.filter(ID=str))>0:
            return False
        else: return True
    except:
        return True
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
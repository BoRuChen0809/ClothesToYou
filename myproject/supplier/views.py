from django.shortcuts import render

# Create your views here.
def sindex(request):
    return render(request, 'supplier_index.html')

def become_partner(request):
    return render(request, 'supplier_become_partner.html')

def slogin(request):
    return render(request, 'supplier_login.html')
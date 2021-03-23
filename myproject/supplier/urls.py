from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.sindex),
    path('sindex/', views.sindex, name='sindex'),
    path('become_partner/', views.become_partner, name='become_partner'),
    path('slogin/', views.slogin, name='slogin'),
    path('slogout/', views.slogout, name='slogout'),
    path('sprofile/', views.sprofile, name='sprofile'),
    path('changespwd/',views.changespwd, name='changespwd'),
    path('changesprofile/',views.changesprofile,name='changesprofile'),
    path('addproduct/' ,views.addproduct,name='addproducte')
]
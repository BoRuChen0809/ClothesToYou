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
    path('changespwd/', views.changespwd, name='changespwd'),
    path('changesprofile/', views.changesprofile, name='changesprofile'),
    path('profileimg', views.profileimg, name='profileimg'),
    path('addproduct/', views.addproduct, name='addproduct'),
    path('editproduct/<str:product_ID>', views.editproduct, name='editproduct'),
    path('sordertrace/<str:order_ID>', views.sordertrace, name='sordertrace'),
    path('supdateorder/', views.supdateorder, name='supdateorder'),
    path('deleteproduct/<str:product_ID>', views.deleteproduct, name='delete')
]
from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.index),
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/',views.logout, name='logout'),
    path('profile/',views.profile, name='profile'),
    path('change_profile',views.changeprofile, name='changeprofile'),
    path('change_pwd', views.changepwd, name='changepwd'),
    path('orders', views.orders, name='orders'),
    path('product/detail/<str:product_ID>', views.product_detail, name='productdetail'),
    path('mycart', views.mycart, name='mycart'),
    path('remove_item/<int:item_ID>', views.remove_from_cart, name='remove_item'),
    path('check_out', views.checkout, name='checkout'),
    path('orderdetails', views.orderdetails, name='confirm'),
    path('orderspage', views.orderspage, name='orderspage'),
    path('orderdetail/<str:order_ID>', views.orderdetail, name='trace_detail'),
    path('cancelorder/<str:order_ID>', views.cancelorder, name='cancel'),
    path('cancelreason/<str:order_ID>', views.cancelreason, name='reason'),
    path('products/<str:category>', views.showproduct_by_tag, name='category'),

    path('search', views.search, name='search'),
    path('searchlist', views.searchlist, name='searchlist'),
]

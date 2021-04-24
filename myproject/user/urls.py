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

    path('search', views.search, name='search'),
    path('searchlist', views.searchlist, name='searchlist'),
    path('cartpage', views.cartpage, name='cartpage'),
]

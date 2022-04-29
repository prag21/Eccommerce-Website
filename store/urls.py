from django.urls import path
from django.urls.resolvers import URLPattern
from .views import home,sign,login,logout,cart,checkout,order
from .middlesware.auth import auth_middleware

urlpatterns=[
    path('',home.as_view(),name='home'),
    path('sign',sign.as_view(),name='sign'),
    path('login',login.as_view(),name='login'),
    path('logout',logout,name='logout'),
    path('cart',cart.as_view(),name='cart'),
    path('checkout',checkout.as_view(),name='c'),
    path('order',auth_middleware(order.as_view()),name='o'),
  
] 
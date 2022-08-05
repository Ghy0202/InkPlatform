#coding-utf-8
from django.conf.urls import url
from .views import RegisterView,LoginView,AdminLoginView

urlpatterns=[
    url(r'^register/$',RegisterView.as_view()),# 前台注册
    url(r'^login/$',LoginView.as_view(),name='HomeLogin'),# 前台登录
    url(r'^admin_login/$',AdminLoginView.as_view(),name='AdminLogin'),# 后台登录
]
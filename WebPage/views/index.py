from django.shortcuts import render
from django.http import HttpResponse
# 重定向
from django.shortcuts import redirect
from django.urls import reverse
from datetime import datetime
from django.db.models import Q
# 弹框
from django.core.paginator import Paginator

from django.contrib import messages

def index(req):
    # 网站首页渲染
    return render(req,'WebPage/index.html')

def contact(req):

    return render(req,'WebPage/contact.html')



def logout(req):
    # 前台退出
    if req.session['homepageuser']:
        del req.session['homepageuser']
    return redirect(reverse("HomeLogin"))
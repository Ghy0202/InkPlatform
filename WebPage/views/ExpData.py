from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
from django.core.paginator import Paginator # 分页
from django.db.models import Q # |查询
# 重定向
from django.shortcuts import redirect
from django.urls import reverse
from userapp.models import *
import os

def show(req):
    # 展示数据
    user = req.session['homepageuser']
    uname = user['uname']
    datas = ExpData.objects
    datalist = datas.filter(username=uname)
    context = {'datalist': datalist}
    return render(req, 'WebPage/ChinaNLP/ExpData_index.html', context)
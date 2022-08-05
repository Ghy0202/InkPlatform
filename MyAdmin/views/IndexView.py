from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.contrib import messages
from userapp.models import * # charm报错但是可以跑通
from django.db.models import Avg, Max, Min, Count, Sum
# 重定向
from django.shortcuts import redirect
from django.urls import reverse
# Create your views here.
class IndexView(View):
    def get(self,request):
        # 后台首页的一些数据
        user_num=UserInfo.objects.filter(state=0).count()
        manage_num=UserInfo.objects.filter(state=6).count()
        scrapy_num=ScrapyData.objects.filter().count()
        exp_num=ExpData.objects.filter().count()

        return render(request,'Admin/Index.html',context={"user_num":user_num,"manage_num":manage_num,"scrapy_num":scrapy_num,"exp_num":exp_num})

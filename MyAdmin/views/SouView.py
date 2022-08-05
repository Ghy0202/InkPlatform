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

class SouIndexView(View):
    def get(self,request):
        return render(request,"Admin/sou.html")
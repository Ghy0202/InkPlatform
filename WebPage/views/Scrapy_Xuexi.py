from django.shortcuts import render
from django.http import HttpResponse
# 重定向
from django.shortcuts import redirect
from django.urls import reverse
import datetime
import time
from django.db.models import Q
# 弹框
from django.core.paginator import Paginator

from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from userapp.models import *

import pandas as pd
import csv
# 导入爬虫模块函数
from .Scrapy_XueXi.Worm import getFromHtml,news_scrapy

def index(request):
    # 学习强国爬虫主页
    return render(request,'WebPage/Experiment_platForm/scrapy_xuexiqiangguo_index.html')


import time


#  生成单号
def get_order_code():
    #  年月日时分秒+time.time()的后7位
    order_no = str(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())) + str(time.time()).replace('.', '')[-7:])
    return order_no

def doScrapy(request):
    FILE_PATH ="./static/Data/"
    # 学习强国执行对应的爬虫任务
    kind = request.POST['type']# 1-新闻 2-活动 3-会议 4-讲话
    num=request.POST['num']# 需要爬取的数量

    # 执行爬虫
    Scrapy_test=news_scrapy(type=kind,num=num)
    json_urls=Scrapy_test.__getJsonUrls__()
    data_i_urls=Scrapy_test.__getChannelDataById__(json_urls)
    c=Scrapy_test.__getContent__(data_i_urls)
    # 获得的内容
    titles=[]
    urls=[]
    contents=[]
    for i in range(len(c)):
        titles.append(c[i][0])
        urls.append(c[i][1])
        contents.append(c[i][2])
    # todo:将爬虫数据保存进csv文件中，同时csv文件名称存入数据库
    user=request.session['homepageuser']
    if user is None:
        print("用户未登录！")
        return render(request, 'WebPage/Experiment_platForm/scrapy_xuexiqiangguo_index.html',{"message":"用户未登录"})
    # 将数据存入csv文件中
    print(user,type(user),get_order_code(),type(get_order_code()))
    csv_file=pd.DataFrame({"title":titles,"content":contents,"url":urls})
    filename=get_order_code()+user['uname'][0:6]+'.csv'
    filepath=FILE_PATH+filename
    csv_file.to_csv(filepath,encoding="utf-8-sig")

    # 将数据存入数据库
    now=datetime.datetime.now()
    scrapy_data=ScrapyData.objects.create(filepath=filepath,filename=filename,create_at=now,username=user['uname'],type=int(kind))
    #return render(request, "WebPage/Experiment_platForm/abstract_index.html", context)
    return render(request, 'WebPage/Experiment_platForm/scrapy_xuexiqiangguo_index.html',{"data":[{'title': t[0], 'url': t[1],'content':t[2]} for t in zip(titles,urls,contents)]})


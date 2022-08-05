
from django.shortcuts import render,HttpResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from userapp.models import * # charm报错但是可以跑通
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse
# https://segmentfault.com/a/1190000041862366?sort=newest
# 这边是用户主页
# 绘图
from pyecharts.charts import Bar, Pie
from pyecharts.faker import Faker
from pyecharts import options as opts
import json

# 摘要部分数据
def show_abstract(req):
    return render(req,'Admin/ExpData/abstract_index.html')
# 摘要分页
def get_abstract_page(request):
    data = ExpData.objects.filter(type=1)
    dataCount = data.count()
    pageIndex = request.GET.get("pageIndex")
    pageSize = request.GET.get("pageSize")
    print("当前索引:{} 当前大小:{}".format(pageIndex, pageSize))
    print("所有记录:{} 数据总条数:{}".format(data, dataCount))

    list = []
    res = []
    for item in data:
        dict = {}
        dict['username'] = item.username
        dict['create_at'] = item.create_at.strftime("%Y-%m-%d %H:%M:%S")
        dict['result'] = item.result
        if len(item.content)>100:
            dict['content']=item.content[0:100]
        else:
            dict['content'] = item.content
        list.append(dict)

    pageInator = Paginator(list, pageSize)
    context = pageInator.page(pageIndex)
    for item in context:
        res.append(item)
    data = {"code": 0, "msg": "ok", "DataCount": dataCount, "data": res}
    return HttpResponse(json.dumps(data))

# 标题部分数据
def show_title(req):
    return render(req,'Admin/ExpData/title_index.html')

def get_title_page(request):
    data = ExpData.objects.filter(type=0)
    dataCount = data.count()
    pageIndex = request.GET.get("pageIndex")
    pageSize = request.GET.get("pageSize")
    print("当前索引:{} 当前大小:{}".format(pageIndex, pageSize))
    print("所有记录:{} 数据总条数:{}".format(data, dataCount))

    list = []
    res = []
    for item in data:
        dict = {}
        dict['username'] = item.username
        dict['create_at'] = item.create_at.strftime("%Y-%m-%d %H:%M:%S")
        dict['result'] = item.result
        if len(item.content) > 100:
            dict['content'] = item.content[0:100]
        else:
            dict['content'] = item.content
        list.append(dict)

    pageInator = Paginator(list, pageSize)
    context = pageInator.page(pageIndex)
    for item in context:
        res.append(item)
    data = {"code": 0, "msg": "ok", "DataCount": dataCount, "data": res}
    return HttpResponse(json.dumps(data))
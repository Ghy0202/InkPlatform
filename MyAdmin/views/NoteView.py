from django.shortcuts import render,HttpResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from userapp.models import * # charm报错但是可以跑通
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse

import json

class NoteIndexView(View):
    def get(self,request):
        return render(request,'Admin/Note/Index.html')

def get_note_page(request):
    # 分页
    data=NoteData.objects.all()
    dataCount = data.count()
    pageIndex = request.GET.get("pageIndex")
    pageSize = request.GET.get("pageSize")
    print("当前索引:{} 当前大小:{}".format(pageIndex,pageSize))
    print("所有记录:{} 数据总条数:{}".format(data,dataCount))

    list = []
    res = []
    for item in data:
        dict = {}
        dict['username'] = item.username
        dict['create_at'] = item.create_at
        dict['title'] = item.title
        dict['content']=item.content
        list.append(dict)

    pageInator = Paginator(list,pageSize)
    context = pageInator.page(pageIndex)
    for item in context:
        res.append(item)
    data = { "code": 0,"msg": "ok","DataCount": dataCount,"data": res }
    return HttpResponse(json.dumps(data))
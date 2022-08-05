from django.shortcuts import render,HttpResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from userapp.models import * # charm报错但是可以跑通
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse

import json

class ScrapyIndexView(View):
    def get(self,request):
        return render(request,"Admin/ScrapyData/Index.html")

def get_scrapy_page(request):
    data = ScrapyData.objects.all()
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
        dict['type'] = item.type
        dict['create_at'] = item.create_at.strftime('%Y-%m-%d %H:%M:%S')
        dict['filepath']=item.filepath
        dict['filename']=item.filename
        list.append(dict)

    pageInator = Paginator(list, pageSize)
    context = pageInator.page(pageIndex)
    for item in context:
        res.append(item)
    data = {"code": 0, "msg": "ok", "DataCount": dataCount, "data": res}
    return HttpResponse(json.dumps(data))

# 删除数据
def del_ScrapyData(request):
    try:
        post_data=json.loads(request.body)

        filename=post_data.get('filename')
        filepath=post_data.get('filepath')
        print(filepath, filename)
        ob=ScrapyData.objects.get(filename=filename)
        import os
        os.remove(filepath)
        ob.delete()
        print(filepath)
    except Exception as err:
        print("失败",err)
    return render(request,"Admin/ScrapyData/Index.html")

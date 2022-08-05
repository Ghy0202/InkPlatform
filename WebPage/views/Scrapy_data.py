# 爬虫数据展示、下载界面
from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
from django.core.paginator import Paginator # 分页
from django.db.models import Q # |查询
# 重定向
from django.shortcuts import redirect
from django.urls import reverse
from userapp.models import *
import os

def show(request):
    # 展示爬虫数据
    user=request.session['homepageuser']
    uname=user['uname']
    datas = ScrapyData.objects
    datalist = datas.filter(username=uname)
    context={'datalist':datalist}
    return render(request,'WebPage/ChinaNLP/scrapyData.html',context)


def scrapy_data_del_one(req):
    try:
        filename = req.POST['filename']
        data = ScrapyData.objects.get(filename=filename)
        filepath = data.filepath
        data.delete()
        os.remove(filepath)
        response = JsonResponse({'status': "成功"})
    except Exception as err:
        response=JsonResponse({"status":"失败","errInfo":str(err)})
    return response


def scrapydata_delSelect(req):
    print("???????????????????????")
    # try:
    filenames = req.POST.getlist('filenames')
    for i in range(len(filenames)):
        filename = filenames[i]
        print("文件名", filename)
        ob = ScrapyData.objects.get(filename=filename)
        ob.delete()
        response = JsonResponse({'status': "成功"})
    # except Exception as err:
    #         print("失败",err)
    #         response = JsonResponse({"status": "失败", "errInfo": str(err)})

    return response
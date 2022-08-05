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
# 文件操作
import os
from io import StringIO
import pandas as pd
import csv
# T5模型
from WebPage.T5_model_pre import predict_func
from userapp.models import *
FILE_PATH='./static/Data/ExpData/'
# 参考：https://blog.csdn.net/color_coral/article/details/90678727
def upload_csv(req):
    if req.method=='GET':
        return render(req,'WebPage/Experiment_platForm/title_t5_index_batch.html')
    else:
        file_obj=req.FILES.get('filename')# 获取文件对象
        file_name=file_obj.name
        print("上传的文件名",file_name)
        # 读取上传的csv文件
        # file_data = file_obj.read().decode("utf-8")
        # csv_data = csv.reader(StringIO(file_data), delimiter=',')
        # for row in csv_data:
        #     print(row)
        #     break
        df_data = pd.read_csv(file_obj)
        contents=df_data['content']
        res_titles=[]
        username = req.session['homepageuser']['uname']
        print("长度",len(contents))
        for i in range(len(contents)):
            if i==0:
                continue
            res_title=predict_func(contents[i])
            res_titles.append(res_title)
            expdata = ExpData.objects.create(username=username, type=0, content=contents[i], result=res_title)
        # 将结果保存起来
        file_path=os.path.join(FILE_PATH+"res_"+file_name)
        csv_file = pd.DataFrame({"res_titles": res_titles, "content": contents[1:]})
        csv_file.to_csv(file_path, encoding="utf-8-sig")
        return render(req,'WebPage/Experiment_platForm/title_t5_index_batch.html',{"data":[{'res_title':t[0],'content':t[1]} for t in zip(res_titles,contents)]})


        # with open(file_path,'wb') as f:
        #     for chunk in file_obj.chunks():
        #         f.write(chunk)

        # 之后再读取csv文件，形成结果csv文件

        #return HttpResponse('ok')

from django.shortcuts import render
from django.http import HttpResponse
# 重定向
from django.shortcuts import redirect
from django.urls import reverse
from datetime import datetime
from django.db.models import Q
# 弹框
from django.core.paginator import Paginator
from userapp.models import *
from django.contrib import messages

from django.shortcuts import render
from django.http import HttpResponse
# T5模型
# from .T5_Models.T5_trained_models.predict_func import predict_func
from WebPage.T5_model_pre import predict_func
def index_t5(req):

    return render(req,'WebPage/Experiment_platForm/title_t5_index.html')

def do_Title_t5(req):
    text=req.POST['text']
    username = req.session['homepageuser']['uname']
    try:
        if text is None:
            messages.error(req, "空句子没发分析哈")
            return redirect(reverse('Title_Index_t5') + "?errinfo=1")
        else:
            title=predict_func(text)
            print("生成的title:",title)
            context={"text":text,"title":title}
            expdata=ExpData.objects.create(username=username,type=0,content=context,result=title)
            return render(req, "WebPage/Experiment_platForm/title_t5_index.html", context)

    except Exception as err:
        print(err)
        messages.error(req, '出错了/(ㄒoㄒ)/~~')
        return redirect(reverse('Title_Index_t5') + "?errinfo=2")


def index_t5_batch(req):
    return render(req, 'WebPage/Experiment_platForm/title_t5_index_batch.html')
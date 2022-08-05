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

from django.shortcuts import render
from django.http import HttpResponse
# 重定向
# T5模型
#from .T5_Models.T5_trained_models.predict_func import predict_func
# T5模型预加载
from WebPage.T5_model_pre import predict_func

from userapp.models import *
# 分词工具包
from snownlp import SnowNLP
import jieba
def index(req):
    username = req.session['homepageuser']['uname']
    user = UserInfo.objects.get(username=username)
    dir_1 = username.split(".")[0]
    context={}
    context['avatar_path'] = './DataBase/' + dir_1 + "/" + user.avatar
    return render(req,'WebPage/Experiment_platForm/abstract_index.html',context=context)

def index_t5(request):
    username = request.session['homepageuser']['uname']
    user = UserInfo.objects.get(username=username)
    dir_1 = username.split(".")[0]
    context={}
    context['avatar_path'] = './DataBase/' + dir_1 + "/" + user.avatar
    return render(request, 'WebPage/Experiment_platForm/abstract_index_t5.html',context=context)

# 处理传过来的句子，生成摘要
def doAbstract(request):
    sentence = request.POST['sentence']
    try:
        if sentence is None:
            messages.error(request, "空句子没发分析哈")
            return redirect(reverse('Abstract_Index') + "?errinfo=1")
        else:
            # 得到分词结果并存储起来
            print(sentence)
            s=SnowNLP(sentence)
            abstract=s.summary(3)
            abstract=abstract[0]
            context = {"sentence": sentence,"abstract":abstract}

            return render(request, "WebPage/Experiment_platForm/abstract_index.html", context)
    except Exception as err:
        print(err)
        messages.error(request, '出错了/(ㄒoㄒ)/~~')
        return redirect(reverse('Abstract_Index') + "?errinfo=2")

# 处理传过来的T5的文本
def doAbstract_t5(request):
    sentence = request.POST['sentence']
    try:
        username = request.session['homepageuser']['uname']
        if sentence is None:
            messages.error(request, "空句子没发分析哈")
            return redirect(reverse('Abstract_Index') + "?errinfo=1")
        else:
            # 得到分词结果并存储起来
            # 这边用T5生成摘要
            model_path='./WebPage/views/T5_Models/T5_trained_models/saved_model/abstract_model'
            abstract = predict_func(model_path=model_path,input_seq=sentence)
            context = {"sentence": sentence, "abstract": abstract}
            # 保存
            expdata=ExpData.objects.create(username=username,type=1,content=context,result=abstract)
            return render(request, "WebPage/Experiment_platForm/abstract_index.html", context)
    except Exception as err:
        print(err)
        messages.error(request, '出错了/(ㄒoㄒ)/~~')
        return redirect(reverse('Abstract_Index') + "?errinfo=2")
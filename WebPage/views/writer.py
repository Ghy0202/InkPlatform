from django.db.models import Q
# 弹框
from django.core.paginator import Paginator

from django.contrib import messages

from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.http import JsonResponse
# T5模型
from .T5_Models.T5_trained_models.predict_func import predict_func
from userapp.models import *
from datetime import datetime
# 将markdown解码为纯文本
import markdown
from bs4 import BeautifulSoup # pip install beautifulsoup4

def article_index(req):
    # todo:筛选出用户的文章列表
    try:
        username = req.session['homepageuser']['uname']
        datas = ArticleData.objects
        datalist = datas.filter(username=username)
        context = {'datalist': datalist}
    except Exception as err:
        context={'datalist':None}


    return render(req, 'WebPage/Experiment_platForm/Article_index.html',context=context)



def unmark(md):
    html = markdown.markdown(md)
    soup = BeautifulSoup(html, features='html.parser')
    return soup.get_text()




def index(req):

    return render(req,'WebPage/Experiment_platForm/Writer_markdown.html')


def generate_t5_title(req):
    text = req.POST['text']
    title = predict_func(text)
    raw_text=unmark(text)

    response = JsonResponse({"status": '标题生成成功', 'title': "生成标题："+title})
    return response


def generate_t5_abstract(req):
    text = req.POST['text']
    raw_text = unmark(text)
    model_path = './WebPage/views/T5_Models/T5_trained_models/saved_model/abstract_model'
    abstract = predict_func(model_path=model_path, input_seq=raw_text)


    response = JsonResponse({"status": '摘要生成成功', 'abstract': "生成摘要：" + abstract})
    return response
def get_Article_id(uname=""):
    import time
    t=time.time()
    id=uname+str(round(t))
    return id

def save(req):
    #TODO: 这边需要创建数据库，具体保存的写法还需要再改
    try:
        text = req.POST['text']
        title = req.POST['title']
        abstract = req.POST['abstract']
        username = req.session['homepageuser']['uname']
        create_at=datetime.now()
        update_at=datetime.now()
        article_id=get_Article_id(username[0:6])
        article=ArticleData.objects.create(title=title,abstract=abstract,content=text,username=username,update_at=update_at,create_at=create_at,article_id=article_id)
        response = JsonResponse({"status": '保存成功'})
        print("保存成功")
    except Exception as err:
        response = JsonResponse({"status": '出错啦:'+str(err)})
        print("保存失败")



    return response


def writer_del_article(req):
    try:
        article_id=req.POST['article_id']
        # 在数据库中查找指定的元素，删除
        oblist=ArticleData.objects.filter(article_id=article_id)
        for ob in oblist:
            ob.delete()
        response = JsonResponse({"status": '删除成功'})
    except Exception as err:
        response = JsonResponse({"status": '删除失败:' + str(err)})

    return response


def writer_download_article(req,article_id=0):
    # 应用实例:https://www.jianshu.com/p/a808b9874579

    ob = ArticleData.objects.get(article_id=article_id)

    content = ob.content
    file_name = ob.article_id + ".txt"
    # 生成txt文件:https://blog.csdn.net/bravezhe/article/details/8501799
    response = HttpResponse(content_type='text/plain')

    response['Content-Disposition'] ='attachment;filename="{}"'.format(file_name)
    response.write(content)


    return response


def writer_edit_article(req,article_id=0):
    ob = ArticleData.objects.get(article_id=article_id)
    print("跳转",article_id)
    return render(req,"WebPage/Experiment_platForm/Writer_edit.html",context={"data":ob.toDict()})


def writer_update(req):
    # 更新文章
    try:
        article_id = req.POST['article_id']
        content = req.POST['content']
        title = req.POST['title']
        abstract = req.POST['abstract']
        ob = ArticleData.objects.get(article_id=article_id)
        ob.title = ob.title
        ob.content = content
        ob.abstract = abstract
        ob.title = title
        ob.update_at = datetime.now()
        ob.save()
        response = JsonResponse({"status": '更新成功'})
    except Exception as err:
        response = JsonResponse({"status": '更新失败'})
    return response


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

class UserIndexView(View):
    def get(self,request):
        return render(request,'Admin/User/Index.html')

def index(request):
    return render(request,"index.html")

def get_page(request):
    # 分页


    data=UserInfo.objects.all()
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
        dict['pwd'] = item.pwd
        dict['state'] = item.state
        list.append(dict)

    pageInator = Paginator(list,pageSize)
    context = pageInator.page(pageIndex)
    for item in context:
        res.append(item)
    data = { "code": 0,"msg": "ok","DataCount": dataCount,"data": res }
    return HttpResponse(json.dumps(data))


def del_User(request):
    # 删除用户
    try:
        #username=request.POST.get["username"]
        post_data = json.loads(request.body)
        username = post_data.get("username")

        ob=UserInfo.objects.get(username=username)
        ob.delete()


    except Exception as err:
        print("失败",err)
    return render(request,'Admin/User/Index.html')


def add_user(request):
    # 添加用户界面
    return render(request,'Admin/User/add.html')

def do_add_user(request):
    # 执行用户添加
    try:
        post_data = json.loads(request.body)
        username = post_data.get("username")
        pwd=post_data.get("pwd")
        state=post_data.get("state")
        state=int(state)
        # 这边需要检查用户名是否合法
        userlist = UserInfo.objects.filter(username=username)
        if userlist:
            # 该用户已经存在
            #TODO：但是后端终止后前端依然是跳出添加成功的字段
            raise Exception("该用户已经存在")
        else:
            user = UserInfo.objects.create(username=username, pwd=pwd,state=state)
            if user:
                # 如果注册成功
                print("注册成功")
            else:
                # TODO：但是后端终止后前端依然是跳出添加成功的字段
                raise Exception('添加失败')


    except Exception as err:
        print("失败")

    return render(request, 'Admin/User/Index.html')


def edit_user(request):
    username=request.GET.get("username")
    state=request.GET.get('state')
    context={'username':username,'state':state}
    return render(request, 'Admin/User/edit.html',context=context)


def do_edit_user(request):
    # 执行用户修改
    try:
        post_data = json.loads(request.body)
        username = post_data.get("username")
        pwd=post_data.get("pwd")
        new_pwd=post_data.get("new_pwd")
        state=post_data.get("state")

        # 这边需要检查用户名是否合法
        userlist = UserInfo.objects.filter(username=username)
        if userlist:
            # 该用户已经存在
            ob = UserInfo.objects.get(username=username)
            if pwd!=ob.pwd:
                print("验证密码错误")
                raise Exception("密码验证错误")
            else:
                ob.state=int(state)
                ob.pwd=str(new_pwd)
                ob.save()
                print("成功")
        else:
            print("该用户不存在")
            raise Exception("该用户不存在")


    except Exception as err:
        print("失败")

    return render(request, 'Admin/User/Index.html')


def logout(request):
    # 管理员退出
    if request.session['adminuser']:
        del request.session['adminuser']
    return render(request,'Admin/login_admin.html')

def response_as_json(data):
    json_str = json.dumps(data)
    response = HttpResponse(
        json_str,
        content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response

######################################################################################################################33
def json_response(data, code=200):
    data = {
        "code": code,
        "msg": "success",
        "data": data,
    }
    return response_as_json(data)


def json_error(error_string="error", code=500, **kwargs):
    data = {
        "code": code,
        "msg": error_string,
        "data": {}
    }
    data.update(kwargs)
    return response_as_json(data)


JsonResponse = json_response
JsonError = json_error


def pie_base() -> Pie:
    data0 = UserInfo.objects.filter(state=0)
    data6=UserInfo.objects.filter(state=6)
    dataCount0 = data0.count()
    dataCount6=data6.count()

    data=[["普通用户",dataCount0],["管理员",dataCount6]]

    c = (
        Pie()
            .add("", data)
            .set_colors(["#191970", "#B22222"])
            .set_global_opts(title_opts=opts.TitleOpts(title="平台使用者统计"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            .dump_options_with_quotes()
    )
    return c

def user_data(request):
    return JsonResponse(json.loads(pie_base()))



# 修改用户信息，密码等
from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
from django.core.paginator import Paginator # 分页
from django.db.models import Q # |查询
# 重定向
from django.shortcuts import redirect
from django.urls import reverse
from userapp.models import *

# 修改用户信息
def edit_personal_info_index(req):
    username=req.session['homepageuser']['uname']
    user=UserInfo.objects.get(username=username)
    context=user.toDict()
    dir_1=username.split(".")[0]
    context['avatar_path']='./DataBase/'+dir_1+"/"+user.avatar
    return render(req,'WebPage/User/edit_index.html',context=context)


# 上传图像并展示
def ajax_avator_upload(req):
    username = req.session['homepageuser']['uname']
    user = UserInfo.objects.get(username=username)


    if req.method=='POST':

        # 更新图像数据
        img=req.FILES.get('avatar')
        # 存用户数据：每个用户开设一个数据文件夹，存放他们的数据
        alist=username.split('.')
        dir_1=alist[0]
        path="./DataBase/"+dir_1+"/"

        import os
        # 如果用户还没有创建自己的数据库，此处创建
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            # 如果之前创建了说明应该是有原始的图片要删除的
            pre_avatar_path=path+"/"+user.avatar
            if os.path.isfile(pre_avatar_path):
                os.remove(pre_avatar_path)

        # 写入用户图片信息
        user.avatar=img.name
        user.save()
        # 修改用户的图像
        avatar_path = "./DataBase/" + user.username.split(".")[0] + "/" + user.avatar
        req.session['homepageuser'] = {"uname": user.username, "avatar_path": avatar_path, "nickname": user.nickname}

        with open(path+img.name,'wb') as f:
            for line in img:
                f.write(line)
        try:
            data={"state":1}
        except:
            data={"state":0}

        return JsonResponse(data)
    return render(req, 'WebPage/User/edit_index.html', context=user.toDict())


def edit_nickname(req):
    try:
        username = req.POST.get('username')
        nickname = req.POST.get('nickname')
        ob = UserInfo.objects.get(username=username)
        print("后台捕获的username:", username)
        print("后台捕获的nickname:", nickname)
        ob.nickname = nickname
        avatar_path = "./DataBase/" + ob.username.split(".")[0] + "/" + ob.avatar
        req.session['homepageuser']={"uname":ob.username,"avatar_path":avatar_path,"nickname":nickname}
        ob.save()
        response = JsonResponse({"status": '更新成功'})
    except Exception as err:
        response = JsonResponse({"status": '更新失败'})
    return response


def edit_personal_pwd_index(req):
    return render(req,"WebPage/User/edit_pwd.html")


def do_edit_pwd(req):
    try:
        oldpwd = req.POST.get('oldpwd')
        newpwd = req.POST.get('newpwd')
        confirmpwd = req.POST.get('confirmpwd')
        print("后台获取oldpwd",oldpwd)
        print(confirmpwd,newpwd,"?")
        if confirmpwd!=newpwd:
            response=JsonResponse({"message":"两次输入的密码不一致","state":0})
            return response
        if len(confirmpwd)<6:
            response = JsonResponse({"message": "密码长度不可以小于6", "state": 0})
            return response
        username = req.session['homepageuser']['uname']
        user = UserInfo.objects.get(username=username)
        print("数据库oldpwd",user.pwd)
        if oldpwd!=user.pwd:
            response = JsonResponse({"message": "旧密码输入错误", "state": 0})
            return response
        user.pwd=newpwd
        user.save()
        response = JsonResponse({"message": "修改成功", "state": 1})
        return response
    except Exception as err:
        response=JsonResponse({"state":0,"message":"服务器错误，请稍后再试"})

    return None


def exam_index(req):
    return render(req,"WebPage/Experiment_platForm/index.html")
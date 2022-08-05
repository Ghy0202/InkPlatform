from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.contrib import messages
from .models import UserInfo
# 重定向
from django.shortcuts import redirect
from django.urls import reverse
# Create your views here.
# 注册
class RegisterView(View):
    def get(self,request):
        return render(request,'WebPage/register_home.html')

    def post(self,request):
        # 获取请求的参数
        uname=request.POST.get('username')
        pwd=request.POST.get('password')
        re_pwd=request.POST.get('repassword')

        # 检查用户名是否重复
        userlist=UserInfo.objects.filter(username=uname)
        if userlist:
            messages.error(request, '该用户已存在')
            return render(request, 'WebPage/register_home.html')
        # 检查密码是否一致
        if len(pwd)<6:
            messages.error(request,'密码长度过短')
            return render(request,'WebPage/register_home.html')
        if re_pwd!=pwd:
            messages.error(request, '密码不一致')
            return render(request, 'WebPage/register_home.html')

        # 加入数据库
        user=UserInfo.objects.create(username=uname,pwd=pwd)
        # 判断是否注册成功
        if user:
            messages.success(request,'注册成功，赶快登录一下~')
            return HttpResponseRedirect('/user/login/')
        else:
            messages.error(request, '不可抗力导致的注册失败~')
            return render(request, 'WebPage/register_home.html')


class LoginView(View):
    def get(self,request):
        return render(request,'WebPage/login_home.html')

    def post(self,request):
        # 执行登录
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        # 检查用户名是否存在
        userlist = UserInfo.objects.filter(username=uname)
        if userlist:
            user = UserInfo.objects.get(username=uname)
            # 检查用户名密码是否正确
            if user.pwd!=pwd:
                messages.error(request, '密码错误')
                return render(request, 'WebPage/login_home.html')
            else:
                # 登录成功
                # 将信息写入cache
                avatar_path="./DataBase/"+uname.split(".")[0]+"/"+user.avatar
                request.session['homepageuser'] = {"uname":uname,"avatar_path":avatar_path,"nickname":user.nickname}
                return redirect(reverse("homeIndex"))
        else:
            messages.error(request, '该用户不存在')
            return render(request, 'WebPage/login_home.html')


class AdminLoginView(View):
    # 后台登录
    def get(self, request):
        return render(request, 'Admin/login_admin.html')

    def post(self,request):
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        verify=request.POST.get('slider')
        print("验证结果",verify)
        if verify=='0':
            messages.error(request, '请拖动滑块验证~')
            return HttpResponseRedirect('/user/admin_login/')

        else:
            # 检查数据库中是否有这个人
            userlist = UserInfo.objects.filter(username=uname)
            if userlist:
                user = UserInfo.objects.get(username=uname)
                # 检查用户名密码是否正确
                if user.pwd != pwd:
                    messages.error(request, '密码错误')
                    return HttpResponseRedirect('/user/admin_login/')
                else:
                    if user.state!=6:
                        #TODO:这边权限只留给管理员
                        messages.error(request, '无权限')
                        return HttpResponseRedirect('/user/admin_login/')
                    else:
                        # 登录成功
                        avatar_path = "./DataBase/" + uname.split(".")[0] + "/" + user.avatar
                        request.session['adminuser'] = {"uname": uname, "avatar_path": avatar_path,
                                                           "nickname": user.nickname}

                        return HttpResponseRedirect('/admin/admin_index/')
            else:
                messages.error(request, '该用户不存在')
                return HttpResponseRedirect('/user/admin_login/')


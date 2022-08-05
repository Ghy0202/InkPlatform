#coding-utf-8

from django.conf.urls import url
from .views.IndexView import IndexView
from .views.UserView import *
from .views.NoteView import *
from .views.ScrapyView import *
from .views.SouView import *
from .views.expView import *

app_name = 'MyAdmin'


urlpatterns=[
    # 管理员退出
    url(r'^admin_logout/$',logout,name="admin_logout"),

    url(r'^admin_index/$',IndexView.as_view(),name='AdminIndex'),# 后台首页

    # 用户信息操作
    url(r'^admin_userInfo/$',UserIndexView.as_view(),name="admin_userInfo"),#后台用户首页
    url(r'^get_page/$',get_page),# 用户分页
    url(r'^delete/$',del_User,name="delete"),# 删除指定用户
    url(r'^add_user/$',add_user,name="add_user"),# 用户添加界面
    url(r'^do_user_add/$',do_add_user,name='do_user_add'),# 执行用户添加
    url(r'^user_edit/$',edit_user,name='user_edit'),# 用户修改界面
    url(r'^do_user_edit/$', do_edit_user, name='do_user_edit'), # 执行用户信息修改

    # 对公告信息的操作
    url(r'^admin_note_Info/$', NoteIndexView.as_view(), name="admin_note_Info"),  # 后台用户首页
    url(r'^get_note_page/$', get_note_page),  # 公告分页
    # url(r'^add_note/$',add_note,name="add_note"),# 公告添加界面
    # url(r'^do_note_add/$',do_add_note,name='do_note_add'),# 执行公告添加

    # 搜索界面
    url(r'^sou/$',SouIndexView.as_view(),name="sou"),

    # 对于爬虫信息的操作：只有删除操作和下载查看操作
    url(r'^admin_scrapy_data/$',ScrapyIndexView.as_view(),name="admin_scrapy_info"),# 后台爬虫信息首页
    url(r'^scpapy_get_page/$',get_scrapy_page),# 分页
    url(r'^delete_scrapy_data_admin/$',del_ScrapyData,name="del_scrapy"),


    # 图表
    url(r'^user_data/$',user_data,name="user_data"),# 首页用户信息

    # 摘要数据：这边都需要做可视化
    url(r'^abstract_index/$',show_abstract,name="abstract_index"),
    url(r'^get_abstract_page/$',get_abstract_page,name="get_abstract_page"),
    # 标题数据：这边也都需要做可视化
    url(r'^title_index/$',show_title,name="title_index"),
    url(r'^get_title_page/$',get_title_page,name="get_title_page"),




]
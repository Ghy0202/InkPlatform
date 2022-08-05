from django.urls import path
from django.contrib import admin
from django.urls import path,include,re_path
from .views import index,Abstract,Scrapy_Xuexi,Title,Scrapy_data,file_utils,writer,homeuser,ExpData
import requests

urlpatterns=[


    # 前台退出
    path('home_logout',index.logout,name='home_logout'),

    path('homeIndex',index.index,name="homeIndex"),#默认的首页
    #path('index',index.index,name="index"),

    # 前台用户信息的维护
    path('edit_personal_info_index',homeuser.edit_personal_info_index,name='edit_personal_info_index'),#展示用户信息修改界面
    path('upload_avatar',homeuser.ajax_avator_upload,name="upload_avatar"),#上传头像单独处理
    path('edit_nickname',homeuser.edit_nickname,name="edit_nickname"),# 修改昵称
    path('edit_personal_pwd_index',homeuser.edit_personal_pwd_index,name="edit_personal_pwd_index"),#修改密码
    path('do_edit_pwd',homeuser.do_edit_pwd,name="do_edit_pwd"),#执行更换密码的操作


    # TODO:前台实验平台首页
    path('exam_index',homeuser.exam_index,name="exam_index"),


    # SnowNLP摘要页面
    path("Abstract_Index",Abstract.index,name="Abstract_Index"),# 实验生成摘要页面
    path("do_Abstract",Abstract.doAbstract,name="do_Abstract"),#生成摘要

    # T5生成摘要页面
    path("Abstract_Index_t5",Abstract.index_t5,name="Abstract_Index_t5"),
    path("do_Abstract_t5",Abstract.doAbstract_t5,name="do_Abstract_t5"),

    # 标题生成页面
    path("Title_Index_t5",Title.index_t5,name="Title_Index_t5"),# 实验标题生成界面
    path("do_t5_generate_title",Title.do_Title_t5,name="do_t5_generate_title"),#T5生成标题：单条
    path("Title_Index_t5_batch",Title.index_t5_batch,name="Title_Index_t5_batch"),#T5生成标题：批量

    # 智能写作界面
    path('Writer_markdown',writer.index,name="Writer_markdown"),
    path('writer_generate_t5_title',writer.generate_t5_title,name="writer_generate_t5_title"),
    path('writer_generate_t5_abstract',writer.generate_t5_abstract,name="writer_generate_t5_abstract"),
    path('writer_save',writer.save,name="writer_save"),
    path("article_index",writer.article_index,name="article_index"),
    path("writer_del_article",writer.writer_del_article,name="writer_del_article"),
    path("writer_download_article/<str:article_id>",writer.writer_download_article,name="writer_download_article"),
    path("writer_edit_article/<str:article_id>",writer.writer_edit_article,name="writer_edit_article"),#编辑文章页面
    path("writer_update",writer.writer_update,name="writer_update"),

    # 上传
    path('upload_csv',file_utils.upload_csv,name="upload_csv"),# 上传csv文件

    # 爬虫页面
    # 学习强国
    path('Scrapy_XueXiQiangGuo_Index',Scrapy_Xuexi.index,name="Scrapy_XueXiQiangGuo_Index"),# 学习强国爬虫主页

    path('do_Scrapy_XueXiQiangGuo',Scrapy_Xuexi.doScrapy,name='do_Scrapy_XueXiQiangGuo'),
    path('scrapy_data_del_one',Scrapy_data.scrapy_data_del_one,name="scrapy_data_del_one"),
    path('scrapydata_delSelect',Scrapy_data.scrapydata_delSelect,name="scrapydata_delSelect"),
    # 数据库展示
    path('show_scrapy_data',Scrapy_data.show,name='show_scrapy_data'),# 展示爬虫数据
    # 展示实验数据
    path('show_exp_data',ExpData.show,name="show_exp_data"),
    # 交流反馈页面
    path("contact",index.contact,name="Contact"),#交流反馈

]
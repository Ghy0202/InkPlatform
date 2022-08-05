from django.db import models
import datetime
# 创建用户表单
class UserInfo(models.Model):
    username=models.EmailField(max_length=100)# 用户帐号是邮箱,唯一标识
    nickname=models.CharField(max_length=50,default="佚名")# 用户昵称
    avatar=models.CharField(max_length=100,default="")#图像名称
    pwd=models.CharField(max_length=100)
    state=models.IntegerField(default=0)# 设置用户状态:0-正常用户 6-管理员

    def __unicode__(self):
        return u"UserInfo:%s"%self.username

    def toDict(self):
        return {"username":self.username,"nickname":self.nickname,"avatar":self.avatar,"pwd":self.pwd,"state":self.state}

# 创建爬虫表单
class ScrapyData(models.Model):
    filepath=models.CharField(max_length=100)# 文件保存路径
    filename=models.CharField(max_length=50)# 文件名
    create_at=models.DateTimeField(default=datetime.datetime.now)
    username=models.CharField(max_length=100)
    type=models.IntegerField(default=0)# 类别：新闻，会议，活动

    def toDict(self):
        return {'create_at':self.create_at.strftime("%Y-%m-%d %H:%M:%S"),'filepath':self.filepath,'type':self.type,'filename':self.filename,'username':self.username}


    # 更改表名
    class Meta:
        db_table="ScrapyData"

# 创建通告表单
class NoteData(models.Model):
    title = models.CharField(max_length=100)  # 通告标题
    create_at = models.DateTimeField(default=datetime.datetime.now)# 创建时间
    username = models.EmailField(max_length=100)  # 创建者
    content=models.EmailField(max_length=600) #通知内容

    def toDict(self):
        return {'title':self.title,"create_at":self.create_at.strftime("%Y-%m-%d %H:%M:%S"),"username":self.username,"content":self.content}

    # 更改表名
    class Meta:
        db_table = "NoteData"


# 创建文本表单
class ArticleData(models.Model):
    article_id=models.CharField(max_length=100,default="anonymous")
    title=models.EmailField(max_length=100)
    abstract=models.CharField(max_length=132)
    create_at = models.DateTimeField(default=datetime.datetime.now)  # 创建时间
    update_at = models.DateTimeField(default=datetime.datetime.now)# 更新时间
    username=models.EmailField(max_length=100)  # 创建者
    content=models.CharField(max_length=1200)

    def toDict(self):
        return {'article_id':self.article_id,
                'title':self.title,
                'abstract':self.abstract,
                "create_at":self.create_at.strftime("%Y-%m-%d %H:%M:%S"),
                "update_at":self.update_at.strftime("%Y-%m-%d %H:%M:%S"),
                "username":self.username,
                "content":self.content}

    class Meta:
        db_table = "ArticleData"

class ExpData(models.Model):
    # 实验数据的记录
    id = models.AutoField(primary_key=True)
    content=models.TextField()
    result=models.CharField(max_length=150)
    type=models.IntegerField()# 0-标题 1-摘要
    create_at=models.DateTimeField(default=datetime.datetime.now)# 创建时间
    username=models.EmailField()

    def toDict(self):
        return {
            "id":self.id,
            "content":self.content,
            "result":self.result,
            "type":self.type,
            "create_at":self.create_at.strftime("%Y-%m-%d %H:%M:%S"),
            "username":self.username
        }
    class Meta:
        db_table = "ExpData"
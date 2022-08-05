# InkPlatform
基于T5的中文摘要、标题生成新闻创作平台
## 关于安装
1. 首先请确保安装了python3以及Mysql,并将项目下载到到本地解压缩
2. 接着进入项目在命令行运行命令``pip install -r requirements.txt``安装本项目所需要的所有依赖包
3. 保证Mysql启动的情况下，修改项目中数据库配置文件信息：数据库名称以及数据库密码
4. 迁移项目中的数据表到本地数据库：python manage.py makemigrations userapp、python manage.py migrate userapp
## 关于项目启动
1. 在项目目录下输入python manage.py runserver
2. 在浏览器输入“http://127.0.0.1:8000/user/login/”即可登录首页，在浏览器输入“http://127.0.0.1:8000/user/admin_login/”即可登录后台（如果暂时没有创建账户，可以先在前台注册）
## 关于摘要生成模型
模型数据比较大，需要的可以在网盘[【传送门】]()下载，将两个文件夹解压缩到"\WebPage\views\T5_Models\T5_trained_models"目录下

from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
from fake_useragent import UserAgent
import os
from urllib import parse
import re
# 爬虫部分参考：https://www.cnblogs.com/lyj153/p/11265475.html
"""解析html格式的数据"""
def getFromHtml(htmldata):
    # 输入html格式的字符串，返回内容
    content_list=re.findall(r'<p class=".*" data-source=".*">(.*?)</p>',htmldata)
    content=""
    for i in range(len(content_list)):
        content+=content_list[i]
    return content


"""爬虫类"""
class news_scrapy(object):

    def __init__(self,type=None,num=5):
        self.__num__=int(num)
        if type==1:
            self.__urls={
                "zhongyaoxinwen": "https://www.xuexi.cn/9ca612f28c9f86ad87d5daa34c588e00/9a3668c13f6e303932b5e0e100fc248b.html",
            }
        elif type==2:
            self.__urls = {
                "zhongyaohuodong":"https://www.xuexi.cn/c06bf4acc7eef6ef0a560328938b5771/9a3668c13f6e303932b5e0e100fc248b.html",
            }
        elif type==3:
            self.__urls = {
                "zhongyaohuiyi":"https://www.xuexi.cn/c06bf4acc7eef6ef0a560328938b5771/9a3668c13f6e303932b5e0e100fc248b.html",
            }
        else:
            self.__urls = {
                "zhongyaojianghua":"https://www.xuexi.cn/588a4707f9db9606d832e51bfb3cea3b/9a3668c13f6e303932b5e0e100fc248b.html",
            }

    def __getJsonUrls__(self,urls=None):
        """
        获取详细的json地址
        """
        urls=self.__urls
        lgDataList=[]
        for key,newsUrls in urls.items():
            js_url_temp=newsUrls.rsplit('/')
            #print(js_url_temp)
            js_url=js_url_temp[0]+"//"+js_url_temp[2]+"/lgdata/"+js_url_temp[3]+"/"+js_url_temp[4].replace("html","json")
            #print(js_url)
            res=requests.get(js_url)
            #print(res)
            res.encoding="utf-8"
            for key,value in json.loads(res.text,encoding='utf-8').items():
                if key=='pageData':
                    item=value['channel']
                    channel_data_url=js_url_temp[0]+"//"+js_url_temp[2]+"/lgdata/"+item['channelId']+'.json'
                    lgDataList.append(channel_data_url)
        return lgDataList

    def __getChannelDataById__(self,lg_urls):
        """
        每个模块获取一定的信息
        """
        data_i_urls=[]
        for lg_url in lg_urls:
            res=requests.get(lg_url)
            res.encoding='utf-8'
            all_values=list(json.loads(res.text,encoding='utf-8'))
            # 这边是用来控制个数的
            for index in range(self.__num__):
                data_i_urls.append(all_values[index]["url"])
        return data_i_urls

    def __getContent__(self,urls):
        """
        获取详细内容:
        得到的是一个列表
        """
        contents=[]
        for url in urls:
            #print("读取地址{0}的数据".format(url))
            js_url_temp=url.rsplit('/')
            if '?id' in url:
                query=dict(parse.parse_qsl(parse.urlsplit(url).query))
                js_url=js_url_temp[0]+'//boot-source.xuexi.cn/data/app/'+query["id"]+'.js'
                res=requests.get(js_url)
                res.encoding="utf-8"
                data=json.loads(res.text.lstrip("callback(").rstrip(")"))
                title=data['title']
                # TODO：格式的提取
                content=getFromHtml(data['content'])
                # print(type(content))
                # print(content)
                contents.append([title,url,content])
            else:
                js_url = js_url_temp[0] + "//" + js_url_temp[2] + "/" + js_url_temp[3] + "/data" + js_url_temp[4].replace("html", "js")
                res=requests.get(js_url)
                res.encoding="utf-8"
                for key,value in json.loads(res.text.lstrip("globalCache=").rstrip(":"),encoding="utf-8").items():
                    if key=="fp8ttetzkclds001":
                        # TODO：格式的提取
                        content=getFromHtml(value["detail"]["content"])

                        # print(type(content))
                        # print(content)
                        title=value["detail"]["frst_name"]
                        contents.append([title,url,content])
        return contents

    def __getLists__(self,urls):
        """
        得到的是三个list
        """
        titles=[]
        urls=[]
        contents=[]
        for url in urls:
            # print("读取地址{0}的数据".format(url))
            js_url_temp = url.rsplit('/')
            if '?id' in url:
                query = dict(parse.parse_qsl(parse.urlsplit(url).query))
                js_url = js_url_temp[0] + '//boot-source.xuexi.cn/data/app/' + query["id"] + '.js'
                res = requests.get(js_url)
                res.encoding = "utf-8"
                data = json.loads(res.text.lstrip("callback(").rstrip(")"))
                title = data['title']
                # TODO：格式的提取
                content = getFromHtml(data['content'])
                # print(type(content))
                # print(content)
                #contents.append([title, url, content])
                titles.append(title)
                urls.append(url)
                contents.append(contents)
            else:
                js_url = js_url_temp[0] + "//" + js_url_temp[2] + "/" + js_url_temp[3] + "/data" + js_url_temp[4].replace("html", "js")
                res = requests.get(js_url)
                res.encoding = "utf-8"
                for key, value in json.loads(res.text.lstrip("globalCache=").rstrip(":"), encoding="utf-8").items():
                    if key == "fp8ttetzkclds001":
                        # TODO：格式的提取
                        content = getFromHtml(value["detail"]["content"])

                        # print(type(content))
                        # print(content)
                        title = value["detail"]["frst_name"]
                        titles.append(title)
                        urls.append(url)
                        contents.append(contents)
        print(len(titles),len(urls),len(contents))
        return titles,urls,contents

    def __file_do__(self,list_info):
        # 将爬取到的信息存到csv文件中
        if not os.path.exists("scrapy_data"):
            os.mkdir("scrapy_data")
        path=r"scrapy_data/data.csv"
        with open(path,'w',encoding="utf-8") as f:
            name=["title","addr","content"]
            file=pd.DataFrame(columns=name,data=list_info)
            file.to_csv(path,encoding='utf_8_sig',index=False)

    def __to_DataBase__(self,list_info):
        # 将读取的数据存入数据库

        pass

    def __show_On_Web__(self,list_info):
        # 将读取的数据展示到web端


        pass

# Scrapy_test=news_scrapy()
# json_urls=Scrapy_test.__getJsonUrls__()
# data_i_urls=Scrapy_test.__getChannelDataById__(json_urls)
# contents=Scrapy_test.__getContent__(data_i_urls)
# Scrapy_test.__file_do__(contents)
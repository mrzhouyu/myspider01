#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@filename:糗事百科.py
#@time：2017-09-24  09:06
#@Author: YU
import urllib.request
from bs4 import BeautifulSoup
import re
import pymysql
import threading
import time


def getHtml(page):
    header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    if page==1:
        url='https://www.qiushibaike.com'
    else:
        url='https://www.qiushibaike.com/8hr/page/'+str(page)+'/'
    try:
        req = urllib.request.Request(url,headers=header)
        res = urllib.request.urlopen(req)
    except:
        print('request is error')
    GET_HTML=res.read().decode('utf8')
    return  GET_HTML#返回得到的源代码

#获取有用标签列表
def Htmllist(html):
    content_list=[]
    soup=BeautifulSoup(html,'html.parser')
    content_div=soup.find_all('div',class_=re.compile('article block untagged mb15'))
    #寻找包含内容的标签存在content_list里后面使用
    for i in content_div:
        if i.find('div',class_='thumb')==None:
            content_list.append(i)
        else:
            continue
    return content_list

#解析获取的标签
def parserHtml(uselist):
    lis_author=[]
    lis_content=[]
    lis_laugh=[]
    lis_argument=[]
    for content_use in uselist :
        #作者名称存入列表
        author_a=content_use.find('h2').string
        lis_author.append(author_a)
        # #获得内容存入列表
        content_div=content_use.find_all('div',class_='content')
        content_string=content_div[0].find('span').string
        lis_content.append(content_string)
        #获得好笑数存入列表
        laugh_span=content_use.find_all('span',class_="stats-vote")
        laugh_string=laugh_span[0].find('i').string
        lis_laugh.append(laugh_string)
        #获取评论数存入列表
        argument_a=content_use.find_all('a',class_='qiushi_comments')
        argument_string=argument_a[0].find('i').string
        lis_argument.append(argument_string)
    return lis_author,lis_argument,lis_laugh,lis_content
#存入数据库
def database(data1,data2,data3,data4):
    #连接数据库 定义全局变量后面关闭数据库和游标
    global con
    global cur
    con=pymysql.connect(host='127.0.0.1',port=3306,user='root',password='915603',db='pythonsql',charset='utf8')
    #获取游标
    cur=con.cursor()
    sql = "INSERT INTO qiushitwo (author,argument,laugh,content) VALUES ( '%s', '%s','%s','%s' )"
    for i,author in enumerate(data1):
        data = (author, data2[i], data3[i],data4[i])
        cur.execute(sql % data)
        con.commit()



if __name__=='__main__':
    threadlis=[]
    pages=int(input('你需要爬取的页数:'))
    #多线程无用版
    # class MYthread(threading.Thread):
    #     def __init__(self,page):
    #         super(MYthread, self).__init__()
    #         self.page=page
    #     def run(self):
    #         getsomehtml=getHtml(self.page)
    #         getsomelist=Htmllist(getsomehtml)
    #         list_content=parserHtml(getsomelist)
    #         print(list_content[0])
    # start_time=time.time()
    # for x in range(0,pages+1):
    #     thread=MYthread(x)
    #     threadlis.append(thread.run())
    # for mythread in threadlis:
    #     mythread.start()
    #     mythread.join()
    #
    # print('多线程爬取结束，花费%s时间'%(time.time()-start_time))

    start_time=time.time()
    for i in range(1, pages + 1):
        lis1=Htmllist(getHtml(i))
        a=parserHtml(lis1)
        print(a[0])
        #下面是保存到数据库
    #     database(a[0],a[1],a[2],a[3])
    #关闭游标和连接
    # cur.close()
    # con.close()
    print('爬取结束,花费了：%s时间'%(time.time()-start_time))

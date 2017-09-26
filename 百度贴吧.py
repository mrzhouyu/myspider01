#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@filename:百度贴吧.py
#@time：2017-09-25  16:05
#@Author: YU
import urllib.request
import re
import time
from bs4 import BeautifulSoup
import queue
import threading
import pymysql

#请求连接部分跟获取用户需要爬取页面数目部分
class response_OP:
    #定义类的参数 某个帖子的初始url 因为下面要实例化两次
    #但是两次需要的功能不一样所以定义静态参数
    #def __init__里定义的是普通参数
    url_lz=''
    #定义一个获取网页源代码方法 返回任何传入的url连接
    def get_response(self,any_url):
        header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
        try:
            req=urllib.request.Request(any_url,headers=header)
            res=urllib.request.urlopen(req)
            HTML=res.read().decode('utf-8')
        except:
            print('RESQUEST IS ERROR')
        return HTML
    #返回一个帖子的总页面数目
    def page_all(self):
        #传入某个楼主的url获取该页面的源代码
        base_html=self.get_response(self.url_lz)
        print('正在获取总页数.....')
        #为了获取总页数而解析
        soup_base=BeautifulSoup(base_html,'html.parser')
        ul=soup_base.find('ul',class_="l_posts_num")
        li=ul.find_all('li')
        span=li[1].find_all('span')
        res_all=span[0].string
        all_pages=span[1].string
        print('恭喜您，获取总页面数成功...')
        print('该贴一共有条%s评论，一共有%s页'%(res_all,all_pages),end='')
        need_page=int(input('。亲，你需要几页的数据，请输入小于等于'+all_pages+'页的数字：'))
        return need_page
#解析所需要数据类
class data_All:

    def get_data_html(self,url3):
        #为了获得请求的方法实例化response_OP类
        my_class2=response_OP()
        #获取该页面的源代码
        page_code=my_class2.get_response(url3)
        #返回源代码
        return page_code
    #写一个处理数据的方法 存入列表 返回一个包含多个列表的元组
    def parser_page(self,url2):
        data_list=[]
        #接收上个方法返回的html给page_html变量
        page_html=self.get_data_html(url2)
        soup_one=BeautifulSoup(page_html,'html.parser')
        print('数据解析中...')
        div_one=soup_one.find_all('div',class_='p_content')
        for everydiv in div_one:
            div_two =everydiv.find('div',class_='d_post_content j_d_post_content ')
            #得到tag里的文字介绍存入列表 了防止爬取到错误的标签而停止加入异常处理
            try:
                data_list.append(div_two.get_text())
            except AttributeError:
                continue
        return data_list

        # 一个清除多余数据的方法 返回一个干净的数据字典

def handell_data(datalist):
    dic = {}
    only_list = []
    # 列表里的列表变成一个列表
    for index1 in datalist:
        only_list += index1
    for index2 in only_list:
        test = re.compile(r'上赛季数据篮板')
        ture_or_false = test.search(index2)
        # 判断是不是符合要求的字符串
        if ture_or_false != None:
            bask_data_list = []
            name = re.findall(r'.*上赛季数据篮板', index2)[0][:-7]
            data_lanban = re.findall(r'篮板\s{0,3}\d{1,2}\.{0,1}\d{0,2}', index2)[0].split('板')[1]
            bask_data_list.append(data_lanban)
            data_zhugong = re.findall(r'助攻\s{0,3}\d{1,2}\.{0,1}\d{0,2}', index2)[0].split('攻')[1]
            bask_data_list.append(data_zhugong)
            data_qiangduan = re.findall(r'抢断\s{0,3}\d{1,2}\.{0,1}\d{0,2}', index2)[0].split('断')[1]
            bask_data_list.append(data_qiangduan)
            data_gaimao = re.findall(r'盖帽\s{0,3}\d{1,2}\.{0,1}\d{0,2}', index2)[0].split('帽')[1]
            bask_data_list.append(data_gaimao)
            data_shiwu = re.findall(r'失误\s{0,3}\d{1,2}\.{0,1}\d{0,2}', index2)[0].split('误')[1]
            bask_data_list.append(data_shiwu)
            data_fangui = re.findall(r'犯规\s{0,3}\d{1,2}\.{0,1}\d{0,2}', index2)[0].split('规')[1]
            bask_data_list.append(data_fangui)
            data_defen = re.findall(r'得分\s{0,3}\d{1,2}\.{0,1}\d{0,2}', index2)[0].split('分')[1]
            bask_data_list.append(data_defen)
            dic[name] = bask_data_list

        else:
            continue
    return dic

#创建一个连接数据库的方法
def connect_mysql(mydic):
    global con
    global cur
    con=pymysql.connect(host='127.0.0.1', port=3306, user='root', password='915603', db='pythonsql',charset='utf8')
    cur=con.cursor()
    sql='TRUNCATE TABLE basktall'
    cur.execute(sql)
    sql="INSERT INTO basktall (name, Lan_ban, zhu_gong, qiang_duan, gai_mao, shi_wu, fan_gui, de_fen) VALUES ('%s',\'%s','%s','%s','%s','%s','%s','%s')"
    for key in mydic:
        data_dic=(key,mydic[key][0],mydic[key][1],mydic[key][2],mydic[key][3],mydic[key][4],mydic[key][5],\
                  mydic[key][6])
        cur.execute(sql%data_dic)
        con.commit()
    cur.close()
    con.close()




if __name__=='__main__':
    url1='https://tieba.baidu.com/p/3138733512?see_lz=1&pn=1'
    #response_OP类的参数实例化
    my_class=response_OP()
    my_class.url_lz=url1
    #获取用户输入页数
    user_page=my_class.page_all()
    #构建一个队列
    global all_url
    all_url = queue.Queue()
    #定义一个全局的总列表
    global text_lis_all
    text_lis_all = []
    #单线程下的爬行效率比较低故这里不用
    # start_time=time.time()
    # for everypage in range(1,user_page+1):
    #     handell_url='https://tieba.baidu.com/p/3138733512?see_lz=1&pn='+str(user_page)
    #     my_class3 = data_All()
    #     text_lis = my_class3.parser_page(handell_url)
    #     text_lis_all += text_lis
    #
    # print('总共花费了%ss'%(time.time()-start_time))

    #下面是多线程爬取
    #获得一个url队列作为下面的参数
    for everypage in range(1,user_page+1):
        handell_url='https://tieba.baidu.com/p/3138733512?see_lz=1&pn='+str(everypage)
        #所有的url存入队列
        all_url.put(handell_url)

    #定义一个线程函数
    def thread_x(get_url):
        # 实例化data_All类
        my_class3 = data_All()
        # 调用parser_page()方法每次返回一个列表 加在一起
        text_lis = my_class3.parser_page(get_url)
        text_lis_all.append(text_lis)
        print('本次进程结束')
    # #返回一个线程列表
    def create_thread():
        thread_list=[]
        while not all_url.empty():
            i=1
            thread_single= threading.Thread(target=thread_x, name='Thread '+str(i) +'号', args=(all_url.get(),))
            thread_single.start()
            thread_list.append(thread_single)
            i=i+1
        return thread_list
    start_time = time.time()
    for mythread in create_thread():
        mythread.join()
    print('总共花费了%ss' % (time.time() - start_time))
    #获得一个需要处理的字典
    get_a_dic=handell_data(text_lis_all)
    #调用函数存入数据库
    connect_mysql(get_a_dic)



















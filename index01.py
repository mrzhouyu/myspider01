#!/usr/bin/env python
# -*- coding:utf-8 -*-
#@filename:index01.py
#@time：2017-09-23  18:27
#@Author: YU
import urllib.request
import http.cookiejar
#获取cookie储存到变量 里
#声明一个CookieJar对象实例来保存cookie
# cookie=http.cookiejar.CookieJar()
# #利用http.cookiejar库的HTTPCookieProcessor对象来创建cookie处理器
# hander=urllib.request.HTTPCookieProcessor(cookie)
# #通过handler来构建opene
# opener=urllib.request.build_opener(hander)
# #此处的open方法同urllib2的urlopen方法，也可以传入request
# res=opener.open('http://www.baidu.com')
# for x in cookie:
#     print(x.name)
#     print(x.value)
#
#
# #获取cookie储存到未文件里
# #设置保存cookie的文件，同级目录下的cookie.txt
# cookiename='cookie.txt'
# #声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
# cookie1=http.cookiejar.MozillaCookieJar(cookiename)
# #利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器
# hander1=urllib.request.HTTPCookieProcessor(cookie1)
# #通过handler来构建opene
# opener1=urllib.request.build_opener(hander1)
# #创建一个请求，原理同urllib2的urlopen
# res1=opener1.open('https://www.zhihu.com/#signin')
# cookie1.save(ignore_discard=True,ignore_expires=True)





# prax=urllib.request.ProxyHandler({'HTTPS':'110.73.32.158:8123'})
# opener=urllib.request.build_opener(prax)
# urllib.request.install_opener(opener)
# req=urllib.request.Request('http://www.baidu.com')
# res=urllib.request.urlopen(req)
# print(res.read().decode('utf-8'))
import queue
import threading
# x=queue.Queue()
# for i in range(0,10):
#     x.put(i)
# def fun1(y):
#     return y
#
# thread1=threading.Thread(target=fun1,args=(x.get(),))
# thread2=threading.Thread(target=fun1,args=(x.get(),))
# thread1.start()
# thread2.start()
# thread1.join()
# thread2.join()
# print(thread2)
# print(thread1)
global lis
lis=[]
print(type(lis))
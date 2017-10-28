#! /usr/bin/env python
# -*- coding=utf-8 -*-
#识别cms、收集子域名、查询C段

import requests,re,threading
import argparse
from tld import get_tld
from lxml import html
import sys
type=sys.getfilesystemencoding()

parser = argparse.ArgumentParser()
parser.add_argument('-u','--url',dest='url',help='eg:http://www.baidu.com')
#parser.add_argument('-o', '--outfile',default='result.txt',dest='outfile')
args = parser.parse_args()

header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}

#识别cms
def bugscaner(url):
	post_url = {'url':url}  #需要发送的post包
	r= requests.post('http://whatweb.bugscaner.com/what/',data=post_url,headers=header)  #发送http post请求
	r_code = r.text
	r_code = eval(r_code)   #获取到的内容为字符串，为了更方便提取所需内容，所以转换成字典形式。
	if r_code['cms'] == '':
		print('Bugscaner无法识别网站：'+url).decode('utf-8').encode(type)
	else:
		print('Bugscaner识别结果：'+url+'使用：'+r_code['cms']).decode('utf-8').encode(type)

#收集子域名
def links(url):
	domain=get_tld(url)#从url中提取域名
	data={'domain':domain,'b2':'1','b3':'1','b4':'1'}
	r=requests.post('http://i.links.cn/subdomain/',data=data,headers=header)
	result=html.fromstring(r.text)
	subdomain=result.xpath("//div[@class='domain']/a/text()")
	#print subdomain
	#print r.text.encode("GBK", 'ignore')
	f=open('subdomain.txt','w')
	for i in subdomain:
		f.write(i+'\n')
		
#查询C段
def webscan(url):
	domain=get_tld(url)
	try:
		url1='http://www.webscan.cc/?action=getip&domain='+domain
		r=requests.get(url=url1,headers=header)
		target1=re.findall('{"ip":"(.*?)",',r.content)#获取ip
		#print target1
		ip='.'.join(target1)
		#print ip
		list=ip.split('.')
		for x in range (1,49):
			list[3]=str(x)#获取c段
			segment='.'.join(list)
			url2='http://www.webscan.cc/?action=query&ip='+segment
			#print url2
			with open('csegment.txt','a') as f:
				r1=requests.get(url=url2,headers=header)
				target2=re.findall('domain":"(.*?)",',r1.content)
				#print target2
				if target2!=[]:
					f.write('********'+segment+'********'+'\n')
					for i in target2:
						f.write(i.replace('\\','')+'\n')
	except:
		pass

def thread(url):
	threads=[]
	#创建线程
	t1=threading.Thread(target=bugscaner(url))
	t2=threading.Thread(target=links(url))
	t3=threading.Thread(target=webscan(url))
	#开启进程
	t1.start()
	t2.start()
	t3.start()
	#添加线程到线程列表
	threads.append(t1)
	threads.append(t2)
	threads.append(t3)
	#等待所有线程完成
	for t in threads:
		t.join()
		
if __name__=='__main__':
	#bugscaner(args.url)
	#links(args.url)
	#webscan(args.url)
	thread(args.url)
	

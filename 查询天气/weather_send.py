#! /usr/bin/env python
# -*- coding=utf-8 -*-

import requests,argparse,codecs
from bs4 import BeautifulSoup
import smtplib  
from email.mime.text import MIMEText  
from email.header import Header

parser = argparse.ArgumentParser()
parser.add_argument('-c','--city',dest='cityname')#指定城市
parser.add_argument('-o', '--outfile',default='w.txt',dest='outfile')#指定保存天气状况的文件，默认为w.txt
parser.add_argument('-m','--mail',dest='receivemail')#指定收件邮箱
args = parser.parse_args()

#获取城市编号
def get_citycode(cityname):
	city={}
	with open("city.txt",'r') as f:
		for line in f:
			line=line.strip().split('\t')
			key=line[1]
			city[key]=line[0]
	citycode=city.get(cityname)
	return citycode

#获取天气状况
def get_content():
	url=('http://www.weather.com.cn/weather/%s.shtml')%citycode
	header={
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
		'Connection':'keep-alive',
		'Accept-Encoding':'gzip, deflate'
	}
	r=requests.get(url,header)
	r.encoding='UTF-8'
	#print r.text
	soup=BeautifulSoup(r.text,'lxml')
	body=soup.body  
	div=body.find('div', id='7d')  #找到id=7d的div
	ul = div.find('ul')  #获取ul部分
	li = ul.find_all('li')  #获取所有的li
	#print li
	final=[]
	for day in li:	# 对每个li标签中的内容进行遍历
		temp=[]
		date = day.find('h1').string  # 找到日期
		temp.append(date)  # 添加到temp中
		weather = day.find_all('p')  # 找到li中的所有p标签
		temp.append(weather[0].string)  # 第一个p标签中的内容（天气状况）加到temp中
		if weather[1].find('span') is None:
			temperature_highest = '无'  # 天气预报可能没有当天的最高气温（到了傍晚，就是这样），需要加个判断语句,来输出最低气温
		else:
			temperature_highest = weather[1].find('span').string  # 找到最高温
		temperature_lowest = weather[1].find('i').string  # 找到最低温
		temp.append(temperature_highest)  # 将最高温添加到temp中
		temp.append(temperature_lowest)  # 将最低温添加到temp中
		#print temp
		final.append(temp)  # 将temp加到final中
	list=[]
	for i in final:
		i='**'.join(i)
		list.append(i)
	f=codecs.open(args.outfile,'w',encoding='utf-8')
	f.write(u'您查询的城市未来7天的天气状况：'+'\r\n')
	for t in list:
		f.write(t+'\r\n')
	f.close()
	f1=open(args.outfile,'r')
	result=f1.read()
	return result

#发送邮件	
def sendmail(content):
	smtpserver="xxx"# 设置smtp服务器
	send_mail="xxx"#发送邮箱
	send_user="xxx"#用户名
	send_pwd="xxx"#口令
	mail_suffix="xxx"#邮箱后缀
	sender="Weather"+"<"+send_user+"@"+mail_suffix+">"
	receiver = [args.receivemail]#收件邮箱
	
	msg = MIMEText(content, 'plain', 'utf-8')
	msg['From'] = sender
	msg['To'] = ','.join(receiver)
	msg['Subject'] = Header(u'来自中国天气网的问候', 'utf-8').encode()
	smtp = smtplib.SMTP_SSL(smtpserver,465)
	smtp.connect(smtpserver)
	smtp.login(send_mail, send_pwd)
	smtp.sendmail(sender, receiver, msg.as_string())
	smtp.quit()

if __name__=='__main__':
	citycode=get_citycode(args.cityname)
	#print citycode
	#get_content()
	sendmail(get_content())






	
	



	
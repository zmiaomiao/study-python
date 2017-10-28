#! /usr/bin/env python
# -*- coding=utf-8 -*-
#爬取可用代理IP

import requests,re
import argparse
from Queue import Queue
import threading
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--page', dest='pagenum', type=int)
parser.add_argument('-t', '--thread', dest='thread', type=int, default=5)
# parser.add_argument('-o', '--outfile', dest='outfile', default='result.txt')
args = parser.parse_args()

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}


class get_proxyip(threading.Thread):
	def __init__(self, que):
		threading.Thread.__init__(self)
		self._que = que

	def run(self):
		while not self._que.empty():
			url = self._que.get()
			r = requests.get(url, headers=header)
			# print r.text
			soup = BeautifulSoup(r.text, 'lxml')
			trs = soup.find_all('tr')
			iplist = []
			for i in range(1, len(trs)):
				tr = trs[i]
				tds = tr.find_all('td')
				# print tds
				# iplist.append(tds[5].text.lower()+'://'+tds[1].text+':'+tds[2].text)
				# print iplist
				try:
					self.avaliable_ip(str(tds[5].text.lower()), str(tds[1].text), str(tds[2].text))#str去除u''
				except Exception, e:
					print e
					pass

				# 验证IP是否可用

	def avaliable_ip(self, type, ip, port):
		proxy = {}
		proxy[type] = 'http://' + ip + ':' + port
		#print proxy
		url = "http://ip.chinaz.com/getip.aspx"
		res = requests.get(url,proxies=proxy)
		result=re.findall("{ip:'(.*?)',",res.text)
		result_ip = ''.join(result)
		#print result_ip
		if ip==result_ip:
			with open('ip.txt', 'a') as f:
				f.write(type+'://'+ip + ':' + port + '\n')


if __name__ == '__main__':
	threads = []
	thread = args.thread
	que = Queue()
	for i in range(1, (args.pagenum + 1)):
		que.put('http://www.xicidaili.com/nn/' + str(i))
	for i in range(thread):
		threads.append(get_proxyip(que))
	for i in threads:
		i.start()
	for i in threads:
		i.join()

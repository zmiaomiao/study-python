# !usr/bin/env python
# -*- coding:utf-8 -*-
#function：12306查票

import argparse,requests,time
import prettytable as pt
from colorama import init, Fore
import sys

init()

date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
#print date
parser = argparse.ArgumentParser() 
parser.add_argument('-f','--from',help='source',dest='fromcity')
parser.add_argument('-t','--to',help='destination',dest='tocity')
parser.add_argument('-d','--date',help='date to go',dest='date',default=date) 
args = parser.parse_args()

def get_citycode(cityname):
	city={}
	with open("r.txt",'r') as f:
		for line in f:
			line=line.strip().split('\t')
			key=line[0]
			city[key]=line[1]
	#print city
	citycode=city.get(cityname)
	return citycode

def getdata():
	url = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT' % (args.date,fromcitycode,tocitycode)
	r=requests.get(url,verify=False)
	available_trains = r.json()['data']['result']
	available_place = r.json()['data']['map']
	#print available_trains
	#print available_place
	for i in available_trains:
		i=i.split('|')
		train_no=i[3]#车次
		duration=i[10]#历时
		train = [
            train_no,
            '\n'.join([Fore.LIGHTGREEN_EX + available_place[i[6]] + Fore.RESET,
                       Fore.LIGHTRED_EX + available_place[i[7]] + Fore.RESET]),
            '\n'.join([Fore.LIGHTGREEN_EX + i[8] + Fore.RESET,
                       Fore.LIGHTRED_EX + i[9] + Fore.RESET]),
            duration,
			i[-4] if i[-4] else '--',#商务座
            i[-5] if i[-5] else '--',#一等座
            i[-6] if i[-6] else '--',#二等座
            i[-12] if i[-12] else '--',#高级软卧
            i[-13] if i[-13] else '--',#软卧
			i[-11] if i[-11] else '--',#动卧
            i[-8] if i[-8] else '--',#硬卧
			i[-9] if i[-9] else '--',#软座
            i[-7] if i[-7] else '--',#硬座
            i[-10] if i[-10] else '--',#无座
        ]
		yield train

def pretty_print():
	tb = pt.PrettyTable([u"车次", u"车站", u"出行时间", u"历时",u"商务座",u"一等",u"二等",u"高级软卧",u"软卧",u"动卧",u"硬卧",u"软座",u"硬座",u"无座"],encoding=sys.stdout.encoding)
	tb.align["车次"]="l"#以车次字段左对齐
	tb.padding_width=1#填充宽度
	#header ='车次 车站 出行时间 历时 一等 二等 高级软卧 软卧 硬卧 硬座 无座'.split()
	#tb._set_field_names(header)
	#tb.field_names = ["车次", "车站", "出行时间", "历时","一等","二等","高级软卧","软卧","硬卧","硬座","无座"]
	for data in train:
		tb.add_row(data)
	print(tb)
	
if __name__=='__main__':
	fromcitycode=get_citycode(args.fromcity)
	tocitycode=get_citycode(args.tocity)
	#print fromcitycode,tocitycode
	train=getdata()
	pretty_print()


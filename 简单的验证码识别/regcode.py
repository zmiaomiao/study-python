# !/usr/bin/env python
# -*- coding:utf-8 -*-
#function:实现简单的验证码识别  读取图片+图像灰度化+二值化+图像文本输出

from PIL import Image
import urllib,re
import StringIO
import pytesseract

url="xxx"#获取验证码的链接
r = urllib.urlopen(url)
#f = open('test.jpg', 'wb')    #这里是将验证码图片写入到本地文件
#f.write(r.read())
#f.close()
imgBuf = StringIO.StringIO(r.read())  # 采用StringIO直接将验证码文件写到内存，省去写入硬盘
img = Image.open(imgBuf)  # PIL库加载图片
img = img.convert('L') 
#print img.format, img.size, img.mode #输出图片属性
#二值化
threshold = 140
table = [] 
for i in range(256): 
	if i < threshold: 
		table.append(0) 
	else: 
		table.append(1) 
out=img.point(table,'1')
#把图片中的字符转化为文本
tessdata_dir_config = '--tessdata-dir "D:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'
text=pytesseract.image_to_string(out, config=tessdata_dir_config)
#print text
code=re.sub("\W","",text)#\W 匹配任意非数字和字母，使验证码中只有字母和数字
if (len(code)==6):
	print code
else:
	pass



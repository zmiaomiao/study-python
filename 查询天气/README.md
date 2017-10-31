脚本实现功能：查询指定城市的未来七天的天气状况，并发送至指定邮箱

效果图：
![weather](https://github.com/zmiaomiao/study-python/blob/master/img/weather.png)

代码中city.txt为中国天气网定义的各个城市的编号，通过中国天气网查询天气并保存至txt文件中，然后再发送至邮箱

Usage：python weather_send.py -h

-c 指定城市，如：-c 上海

-m 指定接收邮箱，如：-m test@qq.com（多个以,隔开）

-o 指定保存天气状况的文件，默认为w.txt

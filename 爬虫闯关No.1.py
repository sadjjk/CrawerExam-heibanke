import requests 
import re 

# 第一关地址：http://www.heibanke.com/lesson/crawler_ex00/
# 你需要在网址后输入数字14901

first_index = 'http://www.heibanke.com/lesson/crawler_ex00/'
number = ''
times = 1

pattern = re.compile(r'<h1>(.*?)</h1>\s<h3>(.*?)</h3>')
number_pattern  = re.compile(r'\d+')

try:
    while True:
        print('第%d次尝试 URL:%s' % (times,(first_index + number)))
        content = re.findall(pattern,requests.get(first_index + number).text)[0]
        
        h1 = content[0]
        h3 = content[1]

        # print(h1)
        print(h3)

        number = re.findall(number_pattern,h3)[0]

        times += 1
        
except:
    print("最终地址是：%s"  % (first_index + number))
    print('END')







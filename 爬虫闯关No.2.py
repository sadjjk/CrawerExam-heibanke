import requests
import random
import re 
# 第二关地址:http://www.heibanke.com/lesson/crawler_ex01/
# 密码:(30以内的数字,猜对它就能过关)

passwords = list(range(31))
pattern = re.compile(r'<h1>(.*?)</h1>\s<h3>(.*?)</h3>')

while True:

    password = random.choice(passwords)
    print('尝试密码:%d' % password)

    data = {
        'username': 'spider',
        'password': password
    }

    content = re.findall(pattern,requests.post('http://www.heibanke.com/lesson/crawler_ex01/',
                            data = data).text)[0]

    h1 = content[0]
    h3 = content[1]

    # print(h1)
    print(h3)

    if '密码错误' in h3:
        passwords.remove(password)
    if '成功' in h3:
        break


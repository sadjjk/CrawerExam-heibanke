import requests
import random
import re 



# 第三关地址:http://www.heibanke.com/lesson/crawler_ex02/
# 还是猜密码  要先登录账号和token 使用Session 账号自行注册

passwords = list(range(31))
pattern = re.compile(r'<h1>(.*?)</h1>\s<h3>(.*?)</h3>')


session = requests.Session()


session.get('http://www.heibanke.com/lesson/crawler_ex02/')

csrftoken1 = session.cookies.get('csrftoken')

account_data = {
    'csrfmiddlewaretoken': csrftoken1,
    'username': 'fikqmw98654',
    'password': '123456'
}

session.post('http://www.heibanke.com/accounts/login/?next=/lesson/crawler_ex02/',
             data = account_data)


csrftoken2 = session.cookies.get('csrftoken')

while True:

    password = random.choice(passwords)
    print('尝试密码:%d' % password)

    data = {
        'csrfmiddlewaretoken': csrftoken2,
        'username': 'spider',
        'password': password
    }


    content = re.findall(pattern,session.post('http://www.heibanke.com/lesson/crawler_ex02/',
                            data = data).text)[0]

    h1 = content[0]
    h3 = content[1]

    # print(h1)
    print(h3)

    if '密码错误' in h3:
        passwords.remove(password)
    if '成功' in h3:
        break

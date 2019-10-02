from PIL import Image
import pytesseract
from io import BytesIO
import requests
import random
import re
from aip import AipOcr


# 第五关:http://www.heibanke.com/lesson/crawler_ex04/
# 验证码 + 猜密码


TIMES = 1


def get_session():
    session = requests.Session()

    session.get('http://www.heibanke.com/accounts/login')

    csrftoken1 = session.cookies.get('csrftoken')

    data = {
        'username': 'fikqmw98654',
        'password': '123456',
        'csrfmiddlewaretoken': csrftoken1,
    }

    session.post('http://www.heibanke.com/accounts/login/',data = data)

    return  session


# 获取验证码和验证码对应的id
def get_captcha(session):
    captcha_string = ''
    while not (len(captcha_string) == 4 and re.findall("[A-Za-z]{4}", captcha_string)):

        captcha_pattern = re.compile(r'<img src="(.*?)" alt="captcha" class="captcha" />')
        captcha_id_pattern = re.compile(r'<input id="id_captcha_0" name="captcha_0" type="hidden" value="(.*?)" />')

        content = session.get('http://www.heibanke.com/lesson/crawler_ex04').text

        captcha_url = 'http://www.heibanke.com/'+ re.search(captcha_pattern,content).group(1)
        captcha_id = re.search(captcha_id_pattern,content).group(1)

        captcha_img_content = requests.get(captcha_url).content

        # tessera-ocr
        # captcha_string = get_captcha_tesseraact(captcha_img_content)

        # baidu-ocr
        captcha_string = get_captcha_baiduOcr(captcha_img_content)

    return captcha_string,captcha_id


def get_captcha_tesseraact(captcha_img_content):

    captcha_img = Image.open(BytesIO(captcha_img_content))

    captcha_string = pytesseract.image_to_string(captcha_img)

    return captcha_string


def get_captcha_baiduOcr(captcha_img_content):

    # 自己申请
    config = {
        'appId': 'XXXXXX',
        'apiKey': 'XXXXXXXXXXXXXX',
        'secretKey': 'XXXXXXXXXXXXXXX'
    }
    client = AipOcr(**config)

    result = client.basicGeneral(captcha_img_content)

    if 'words_result' in result:
        return ''.join([w['words'] for w in result['words_result']])


# 尝试登陆
def test(data):
    global TIMES
    pattern = re.compile(r'<h3>(.*?)</h3>')
    captcha_string, captcha_id = get_captcha(session)
    data['captcha_0'], data['captcha_1'] = captcha_id, captcha_string
    print("第%d次尝试,验证码:%s,密码:%d" % (TIMES, captcha_string, password))

    h3 = re.search(pattern, session.post('http://www.heibanke.com/lesson/crawler_ex04/',
                                         data=data).text).group(1)

    print(h3)

    TIMES += 1

    return h3



if __name__ == '__main__':

    passwords = list(range(31))

    session = get_session()


    while True:
        password = random.choice(passwords)

        captcha_string,captcha_id = get_captcha(session)

        data = {
            'csrfmiddlewaretoken': session.cookies.get('csrftoken'),
            'username': 'spider',
            'password': password
        }

        h3 = test(data)

        while  ('验证码输入错误' in h3):
            h3 = test(data)

        if '密码错误' in h3:
            passwords.remove(password)
        if '成功' in h3:

            break




# from aip import AipOcr
#
# config = {
#     'appId': '17402632',
#     'apiKey': '9vIQ9uVmGiBkoHtqGYI1dsTY',
#     'secretKey': 'W7cIjUq0Ce1G443Mb7y7zvsLbuL4UEGY'
# }
#
#
# # APP_ID = '16909218'
# # API_KEY = 'NsrhtcVxDym1AOXDqZfd36nz'
# # SECRET_KEY = 'gVemv3TfPlrtMHBvpXW6MpqU0qjLfu3W'
#
# client = AipOcr(**config)
#
# def get_file_content(file):
#     with open(file, 'rb') as fp:
#         return fp.read()
#
# def img_to_str(image_path):
#     image = get_file_content(image_path)
#     result = client.basicGeneral(image)
#     if 'words_result' in result:
#         return '\n'.join([w['words'] for w in result['words_result']])
#
#
# print(img_to_str('3.png'))
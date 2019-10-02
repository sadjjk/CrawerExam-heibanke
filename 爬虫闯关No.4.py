import requests
import re 


# 第四关:http://www.heibanke.com/lesson/crawler_ex03/
# 拼接密码

session = requests.Session()

session.get('http://www.heibanke.com/accounts/login')

csrftoken1 = session.cookies.get('csrftoken')

data = {
	'username': 'fikqmw98654',
	'password': '123456',
	'csrfmiddlewaretoken': csrftoken1,
}

session.post('http://www.heibanke.com/accounts/login/',data = data)

pattern = re.compile(r'<td data-toggle="tooltip" data-placement="left" title="password_pos">(\d+)</td>\s*<td data-toggle="tooltip" data-placement="left" title="password_val">(\d+)</td>')

password_dict = {}

while  len(password_dict) < 100:

	content = session.get('http://www.heibanke.com/lesson/crawler_ex03/pw_list/').text

	password_couple = re.findall(pattern,content)

	for (password_pos,password_val) in password_couple:

		if password_pos not in password_dict.keys():
			password_dict[int(password_pos)] = int(password_val)

	print("共100位密码，已获得%d位密码" % len(password_dict))

# print(password_dict)

password = ''.join(str(i[1]) for i in sorted(password_dict.items()))

print("密码是：%s" % password)


pattern = re.compile(r'<h1>(.*?)</h1>\s+<h3>(.*?)</h3>')

session.get('http://www.heibanke.com/lesson/crawler_ex03/')

csrftoken2 = session.cookies.get('csrftoken')

data = {
	'username': 'aaa',
	'password': password,
	'csrfmiddlewaretoken': csrftoken2
}


content = re.findall(pattern,session.post('http://www.heibanke.com/lesson/crawler_ex03/',
                            data = data).text)[0]

print(content)

h1 = content[0]
h3 = content[1]

print(h1)
print(h3)


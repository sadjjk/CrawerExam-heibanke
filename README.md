# 黑板客爬虫闯关通关

爬虫学的好 牢房进的早   

### 前言

黑板客爬虫闯关共5关 

- http://www.heibanke.com/lesson/crawler_ex00/
- http://www.heibanke.com/lesson/crawler_ex01/
- http://www.heibanke.com/lesson/crawler_ex02/
- http://www.heibanke.com/lesson/crawler_ex03/
- http://www.heibanke.com/lesson/crawler_ex04/

网上关于这部分的代码实践也不少    
绝知此事要躬行  自己code一遍 

### 第一关

![UTOOLS_COMPRESS_1569999755672.png](https://i.loli.net/2019/10/02/hAwDifI4vkNtge9.png)

`requests` GET 不断请求即可

```
下一个你需要输入的数字是25997. 老实告诉你吧, 这样的数字还有上百个
第49次尝试 URL:http://www.heibanke.com/lesson/crawler_ex00/25997
下一个你需要输入的数字是73222. 老实告诉你吧, 这样的数字还有上百个
第50次尝试 URL:http://www.heibanke.com/lesson/crawler_ex00/73222
下一个你需要输入的数字是93891. 老实告诉你吧, 这样的数字还有上百个
第51次尝试 URL:http://www.heibanke.com/lesson/crawler_ex00/93891
恭喜你,你找到了答案.继续你的爬虫之旅吧
最终地址是：http://www.heibanke.com/lesson/crawler_ex00/93891
END
```

### 第二关

![UTOOLS_COMPRESS_1569999938435.png](https://i.loli.net/2019/10/02/Hx8YCN2kVrt9qcJ.png)

猜密码 这里从0~30的列表中 `random.choice`每次随机给出一个数     
若此数密码不正确 则从该列表中remove

```
尝试密码:13
您输入的密码错误, 请重新输入
尝试密码:5
您输入的密码错误, 请重新输入
尝试密码:10
您输入的密码错误, 请重新输入
尝试密码:8
恭喜! 用户spider成功闯关, 继续你的爬虫之旅吧
```

### 第三关

![Xnip2019-10-02_15-10-41.jpg](https://i.loli.net/2019/10/02/vtEu8UbP31Dgfy7.jpg)

第三关先进去是这样的 没有谜题 一头雾水     
需要先在这里注册账号 登陆后重新打开 出现谜题

![UTOOLS_COMPRESS_1570000211937.png](https://i.loli.net/2019/10/02/scdnE5CUTq6l4WH.png)

还是猜密码 第一反应就是要先登陆 requests Session 模拟登陆即可   
但是没有成功 谜题写着两层保护 也没看懂     
百度后 明白了 还有一层token的加密

![UTOOLS_COMPRESS_1570000617203.png](https://i.loli.net/2019/10/02/DmY3XNvFhueLkRJ.png)

首先是账号登陆时需要一个token    
其次是谜题猜密码时也需要一个token  
这里两个token均来自cookies

```python
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
```

两次token不同  需重新获取 然后就是熟悉的猜密码 和第二关相同

### 第四关

![uaxydA.png](https://s2.ax1x.com/2019/10/02/uaxydA.png)

依然一脸懵逼 尝试输入密码 提示密码在这里寻找

![UTOOLS_COMPRESS_1570001394116.png](https://i.loli.net/2019/10/02/LaCRexzIHTGjnom.png)

注意：并不把所有13页的密码按照<位置,值>拼起来就组成最终的密   码，因为有些位置会重复给出 可能加载完所有页 也不一定组成出完整的密码 可能还是会有个别位置缺失     
PS:第一次尝试就是把所有页爬下来 拼密码 发现存在个别位置缺失  
其实只要第一页反复刷新就可以了     
直到所有密码(共100位 页面探索所得)都有拼上为止

当然拼密码之前 需要模拟登陆 熟悉的配方        
经过漫长的登陆 终于获得所有位置的密码

```
共100位密码，已获得99位密码
共100位密码，已获得99位密码
共100位密码，已获得99位密码
共100位密码，已获得100位密码
密码是：5357748950695244329548946136479903948743260484371348776618136963449163264706489936702831052533819016
恭喜! 用户aaa成功闯关, 继续你的爬虫之旅吧
```

### 第五关

![UTOOLS_COMPRESS_1570001895588.png](https://i.loli.net/2019/10/02/EIbCJ5zMXGgfvo4.png)

加了验证码 验证码使用OCR识别出正确的字母 这里的图片已经很清晰 不用二值化或灰度处理 唯一的问题就是个别字母倾斜导致OCR识别错误 暂时不知道如何倾斜矫正    

OCR使用 pytesseract或者百度OCR  两者的识别准确率半斤八两 都不太高 基本都出错在倾斜字母上 但总体上还是能用

tips:不用把每次的验证码图片下载下来 会下载很多验证码 以后也不会用到 浪费空间  直接获得验证码图片的二进制content 每次拿二进制content去识别

当然验证码识别之前 需要模拟登陆 密码也是30以内的数字 熟悉的配置 

经过漫长的等待

```
第1次尝试,验证码:CINR,密码:3
验证码输入错误
第2次尝试,验证码:SSMO,密码:3
恭喜! 用户spider成功闯关, 后续关卡敬请期待
```

### END

[Code](https://github.com/sadjjk/CrawerExam-heibanke):https://github.com/sadjjk/CrawerExam-heibanke

[Blog](https://sadjjk.github.io/)    [Stock](http://47.105.166.237/index)


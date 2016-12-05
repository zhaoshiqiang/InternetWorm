import gzip
import re
import http.cookiejar
import urllib.request
import urllib.parse

def ungzip(data):
    try:
        print('正在解压....')
        data = gzip.decompress(data)
        print('解压完毕')
    except:
        print('未经解压，无需解压')
    return data

def getXSTF(data):
    cer = re.compile('name="_xsrf" value="(.*)"',flags= 0)
    strlist = cer.findall(data)
    return strlist

def getOpener(head):
    # deal with the Cookies
    cj = http.cookiejar.CookieJar()
    pro = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(pro)
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener

header = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Accept-Encoding': 'gzip, deflate',
    'Host': 'www.zhihu.com',
    'DNT': '1'
}

url = 'http://www.zhihu.com'
opener = getOpener(header)
op = opener.open(url)
data = op.read()
#知乎首页传回来的数据需要解压缩
data = ungzip(data)
#_xsrf这个值是知乎首页传回来的，再次发送请求时需要将这个值带上
_xsrf = getXSTF(data)

url += 'login'
id = '13716027713'
password = 'zhaoshiqiang'
postDict = {
    '_xsrf':_xsrf,
    'email':id,
    'password':password,
    'rememberme':'y'
}
'''
urllib.parse 库里的 urlencode() 函数. 这个函数可以把 字典 或者 元组集合 类型的数据转换成 & 连接的 str
str 还不行, 还要通过 encode() 来编码, 才能当作 opener.open() 或者 urlopen() 的 POST 数据参数来使用.
'''
postData = urllib.parse.urlencode(postDict).encode()
op = opener.open(url, postData)
data = op.read()
data = ungzip(data)

print(data.decode())
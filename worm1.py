import urllib.request
import urllib
import re
from _collections import deque

queue = deque()
visited = set()

url = 'http://news.dbanotes.net'

queue.append(url)
cnt = 0

while queue:
    url = queue.popleft()
    visited |={url}
    print('已经抓取' + str(cnt) + '   正在抓取 <---  ' + url)
    cnt += 1
    #添加超时，当一些网站上不了时则跳过
    try:
        urlop = urllib.request.urlopen(url,timeout=2)
    except :
        continue
    '''
        这个版本的正则表达式是'href="(.+?)"'
        这个正则表达式会把那些.ico或者.jpg的链接都爬下来. 这样read()了之后碰上decode(‘utf-8′)就要抛出异常.
        因此我们用getheader()函数来获取抓取到的文件类型从而判断是不是html类型，如果是则继续分析其中链接
    '''
    if 'html' not  in urlop.getheader('Content-Type'):
        continue
    '''
    即使前面加了判断，依然有些网站运行decode()会异常. 因此我们把decode()函数用try..catch语句包围住, 这样他就不会导致程序中止
    '''
    try:
        data = urlop.read().decode('utf-8')
    except:
        continue

    linkre = re.compile('href=\"(.+?)\"')
    for x in linkre.findall(data):
        if 'http' in x and x not in visited:
            queue.append(x)
            print('加入队列 --->  ' + x)
'''
爬虫是可以工作了, 但是在碰到连不上的链接的时候, 它并不会超时跳过.
而且爬到的内容并没有进行处理, 没有获取对我们有价值的信息, 也没有保存到本地.
 下次我们可以完善这个alpha版本.
'''

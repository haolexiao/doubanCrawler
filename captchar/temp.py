#-*-coding:utf-8-*- #编码声明，不要忘记！
import requests  #这里使用requests，小脚本用它最合适！
from lxml import html
import thread
import time
import codecs
url = 'https://kkembed.kdwcl.com/share/'
headers = {

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
}
gap = 5000
mark = 0
fout = codecs.open('test.csv', 'a', encoding='utf-8')
def crawler(i):
    try:
        pageURL = url+str(i)
        page = requests.get(pageURL,headers = headers)
        tree = html.fromstring(page.text)
        title_name = tree.xpath('head/title/text()')[0]
        print i, title_name

        if title_name == u'您访问的页面不存在或已被删除':
            mark = 1
        else:
            fout.write(str(i) + "," + title_name+'\n')
    except:
        print 'error'


try:
    i = 5000
    while i<10000:
        if mark == 1:
            i = i+500
            mark = 0
        for k in xrange(8):
            thread.start_new_thread(crawler, (i*8+k,))
        i = i+1
        time.sleep(6)

except:
    print "Error: unable to start thread"


while 1:
   pass





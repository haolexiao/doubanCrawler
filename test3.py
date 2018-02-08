#-*-coding:utf-8-*- #编码声明，不要忘记！
import random

import requests  #这里使用requests，小脚本用它最合适！

import codecs
import Queue
import json

import time
from lxml import html    #这里我们用lxml，也就是xpath的方法


from PIL import Image
import matplotlib.pyplot as plt

import os

visited_user=set()
visited_movie = set()
visited_book  = set()
usr = Queue.Queue()


dict_id_name = {}

main_url = 'https://www.douban.com'
raw_cookies = [
    '__utmc=30149280; ck=H9Il; __utmz=30149280.1514993519.3.2.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/accounts/login; ll=108288; _vwo_uuid_v2=E90AE2022436CBF2CEEED90E00046AAF|b2852a314962cc64ec7da44db1f5de1c; bid=JfD9o8vzOyE; __utma=30149280.364165925.1513543666.1517858156.1517881884.9; ue=zhangzhao199323@yahoo.com.cn; gr_user_id=763ad491-bf3c-4d14-a97b-44bf1966a296; __utmv=30149280.17360; ps=y; dbcl2=173607767:0ToXQ/kCi/4; ct=y; __utmb=30149280.2.10.1517881884; __utmt=1; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1517881884%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D_RxfZwmGoUvBiqis7kpMV6JbGA14SMGdnDFt2kMv5pBXdtQuiIFXTg1rnQN6oc9n%26wd%3D%26eqid%3Dedc80f050001da45000000035a77ceab%22%5D; _pk_id.100001.8cb4=38273b39dc5d7a3d.1513543666.8.1517881884.1517858191.; _pk_ses.100001.8cb4=*',
    'll="108288"; bid=mCEK2EAt_J4; __yadk_uid=Z914VtOVBusejcOvRDCF5zwkGYe8uNYJ; push_noty_num=0; push_doumail_num=0; __utmc=30149280; __utmz=30149280.1517854308.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=30149280.17361; ap=1; ps=y; __utma=30149280.944334073.1517854308.1517854308.1517857862.2; dbcl2="173611196:ywTKV4HJgZY"; ck=-cHY; _pk_id.100001.8cb4=a252f16f265a0f30.1517854257.4.1517881865.1517861420.; _pk_ses.100001.8cb4=*'
]

headers = [
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'},
    {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; Touch; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; Tablet PC 2.0)'}
]
def get_proxies():
    pass

def pause():
    time.sleep(5 + 3*random.random())
    return


def fobbiden_check(tree, original_url, cookie):
    title_name = tree.xpath('head/title/text()')
    while title_name[0] == u'403 Forbidden':
        print '403 Forbidden'
        proxies = get_proxies()
        page_follow = requests.get(original_url, cookies=cookie, proxies=proxies)



    if title_name[0] == u'\u7981\u6b62\u8bbf\u95ee':
        captcha = tree.xpath("//img[@alt='captcha']/@src")
        captcha_id = captcha[0].split('=')[1]
        localpath = "captchar/captchar.jpg"
        print captcha[0]
        ir = requests.get(captcha[0])
        if ir.status_code == 200:
            with open(localpath, 'wb') as file:
                file.write(ir.content)
            #open('captchar.jpg', 'wb').write(ir.content)
        #urllib.request.urlretrieve(captcha[0], filename=localpath)
        with open(localpath, 'rb') as f:
            img = Image.open(f)
            plt.figure("captchar")
            plt.imshow(img)
            plt.show()
            plt.close()
        #f.close()
        captcha_value = raw_input("请查看本地验证码图片并输入验证码")
        os.rename(localpath, 'captchar/'+captcha_value+'.jpg')

        data = {
            "ck": "NhlJ",
            "captcha-solution": captcha_value,
            "captcha-id": captcha_id,
            "original-url": original_url
        }
        page = requests.post('https://www.douban.com/misc/sorry', cookies = cookie, data = data)
        if page.status_code == 200:
            print 'success'
            tree = page


def follow_crawler(url, info_follow, cookie, header, usr_queue, dict_id_name, tmp_usr = ""):
    if url[0] == '/':
        url = main_url+url
    print url
    try:
        #proxies = {"http": "182.103.247.207:808", "https": "182.103.247.207:808" }
        #page_follow = requests.get(url, cookies=cookie, proxies=proxies)
        #hea = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}

        #page_follow = requests.get(url, cookies=cookie, proxies=proxies)
        page_follow = requests.get(url, cookies=cookie, headers=header)
        tree = html.fromstring(page_follow.text)
        print tree.xpath('head/title/text()')[0].strip()
        if tmp_usr != "":
            dict_id_name[tmp_usr] = tree.xpath('head/title/text()')[0].strip()[:-4]

        fobbiden_check(tree, url, cookie)
        intro_raw = tree.xpath('//dl[@class="obu"]/dd/a')
        #print tree.xpath('head/title/text()')[0]
    except:
        print page_follow.text

    for x in intro_raw:
        tmp_follow_name = x.xpath('@href')[0].split('/')[4]
        tmp_nick_name = x.xpath('text()')[0]
        #print tmp_nick_name
        info_follow.append(tmp_follow_name)
        usr_queue.put(tmp_follow_name)
        dict_id_name[tmp_follow_name] = tmp_nick_name

    info_next = tree.xpath('//div[@class="paginator"]/span[@class="next"]/link/@href')
    if len(info_next) == 1:
        pause()
        return follow_crawler(info_next[0], info_follow, cookie, header, usr_queue, dict_id_name)

    
def book_crawler(url, cookie, header, visited_book, book_list):
    if url[0] == '/':
        url = main_url+url
    print url
    try:
        page_book = requests.get(url, cookies=cookie, headers=header)
        tree = html.fromstring(page_book.text)
        fobbiden_check(tree, url, cookie)

        intro_raw = tree.xpath('//li[@class="subject-item"]/div[@class="info"]')
    except:
        print page_book.text

    for x in intro_raw:
        tmp_book_id = x.xpath('h2/a/@href')[0].split('/')[4]
        book_title = x.xpath('h2/a/@title')[0]
        rating = x.xpath('div[@class="short-note"]/div/span/@class')[0]
        #print book_title

        if rating[0] == 'r':
            #print x.xpath('h2/a/@title')[0]
            date = x.xpath('div[@class="short-note"]/div/span[@class="date"]/text()')[0].split('\n')[0]
            rating = int(rating[6])
            visited_book.add(tmp_book_id)

            info_item = {'id': tmp_book_id, 'name': book_title, 'rating': rating, 'date': date}
            book_list += [info_item]


    info_next = tree.xpath('//div[@class="paginator"]/span[@class="next"]/link/@href')
    if len(info_next) == 1:
        pause()
        book_crawler(info_next[0], cookie, header, visited_book, book_list)

def movie_crawler(url,cookie, header, visited_movie, movie_list):
    if url[0] == '/':
        url = main_url+url
    print url
    try:
        page_movie = requests.get(url, cookies=cookie, headers=header)
        tree = html.fromstring(page_movie.text)
        fobbiden_check(tree, url, cookie)
        intro_raw = tree.xpath('//div[@class="item"]/div[@class="info"]')
    except:
        print page_movie.text


    for x in intro_raw:
        #print x.text
        #print x.xpath('ul/li[@class="title"]/a/@href')

        tmp_movie_id = x.xpath('ul/li[@class="title"]/a/@href')[0].split('/')[4]
        movie_title = x.xpath('ul/li[@class="title"]/a/em/text()')[0]
        #print movie_title

        rating = x.xpath('ul/li[3]/span/@class')[0]
        if rating[0] == 'r':
            #print x.xpath('h2/a/@title')[0]
            date = x.xpath('ul/li/span[@class="date"]/text()')[0].split('\n')[0]
            rating = int(rating[6])
            visited_movie.add(tmp_movie_id)
            #print date
            info_item = {'id': tmp_movie_id, 'name': movie_title, 'rating': rating, 'date': date}
            #print info_item
            movie_list+= [info_item]


    info_next = tree.xpath('//div[@class="paginator"]/span[@class="next"]/link/@href')
    if len(info_next) == 1:
        pause()

        movie_crawler(info_next[0], cookie, header, visited_movie, movie_list)

def SelectCookie():
    cookies = raw_cookies[random.randint(0,1)]
    cookie= {}
    for line in cookies.split(';'):
        key, value = line.split("=", 1)
        cookie[key] = value #一些格式化操作，用来装载cookies
    return cookie,headers[random.randint(0,1)]

def crawler():
    #豆瓣模拟登录，最简单的是cookie，会这个方法，80%的登录网站可以搞定
    cookie = {}
    random.seed(10)
    #raw_cookies = "bid=DZdKXz5FCzQ; __utmc=30149280; __yadk_uid=azyN1oel963FzdER9jIAL3TGWDgeP9rp; __utmz=30149280.1514902739.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ps=y; push_noty_num=0; push_doumail_num=0; __utmv=30149280.5439; ap=1; ll=\"108288\"; ck=eo0t; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1514983918%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DgeJQw9nT77EkTAt2MPhHO0-KS_TOlbdM9CQjFknNCEMQ_dGtwdbg2HnmhhJj3FN3w4kLh2uILJw267VBlSAtqa%26wd%3D%26eqid%3Db0e7f49d00014fc4000000035a4b94cd%22%5D; _pk_ses.100001.8cb4=*; __utma=30149280.1127883720.1514737149.1514967864.1514983919.4; __utmt=1; __utmb=30149280.9.5.1514983919; _pk_id.100001.8cb4=7641a25d78110bdb.1514737147.5.1514984744.1514976634."
    #raw_cookies = "bid=DZdKXz5FCzQ; __utmc=30149280; __yadk_uid=azyN1oel963FzdER9jIAL3TGWDgeP9rp; __utmz=30149280.1514902739.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ps=y; ck=NhlJ; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1514967843%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DgeJQw9nT77EkTAt2MPhHO0-KS_TOlbdM9CQjFknNCEMQ_dGtwdbg2HnmhhJj3FN3w4kLh2uILJw267VBlSAtqa%26wd%3D%26eqid%3Db0e7f49d00014fc4000000035a4b94cd%22%5D; _pk_ses.100001.8cb4=*; push_noty_num=0; push_doumail_num=0; __utma=30149280.1127883720.1514737149.1514902739.1514967864.3; __utmv=30149280.5439; ap=1; _pk_id.100001.8cb4=7641a25d78110bdb.1514737147.3.1514970462.1514903130.; __utmb=30149280.18.10.1514967864"
    #raw_cookies = 'bid=kAmCNYHrbEQ; ll="108288"; __yadk_uid=eDKBwgFywkEuSH4GgAjCnTsGzXWvmRQQ; gr_user_id=8b496285-0cee-4301-a180-d2b83bd13cb4; _ga=GA1.2.2044174053.1498494277; viewed="26287433_1432816_6709809"; _vwo_uuid_v2=D872348775F22E1F84386CF7E44B619A|8bdd0c8fd8b1c74684878ce9cdf244f1; __utmc=30149280; __utmv=30149280.5439; push_doumail_num=0; __utmz=30149280.1513352768.16.15.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; dbcl2="54390901:mQqoe0JhdEI"; ck=NhlJ; ap=1; ps=y; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1513543651%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DxA9VQozh8Iwd6h4Z52nE85Oq9-osLrEFT0V4oWrNy0p2jHUZGz9othZsS-A_CvDhCoVFrPgZEkOysj_-94Tssa%26wd%3D%26eqid%3D90b349a700032896000000035a33ee37%22%5D; _pk_ses.100001.8cb4=*; __utma=30149280.2044174053.1498494277.1513540130.1513543670.19; _pk_id.100001.8cb4=8f8463fa2e8d42d8.1498494275.32.1513544372.1513540419.; push_noty_num=0; __utmt=1; __utmb=30149280.6.10.1513543670'#引号里面是你的cookie，用之前讲的抓包工具来获得


    #cookie =  {'cookie': raw_cookies}
    #重点来了！用requests，装载cookies，请求网站
    url = {'movie':'https://movie.douban.com/people/','book':'https://book.douban.com/people/','follow':'https://www.douban.com/people/'}


    fout = codecs.open('usr_info.txt', 'a', 'utf_8_sig')
    while not usr.empty():
        tmp_usr = usr.get();
        if tmp_usr not in visited_user:
            print tmp_usr
            visited_user.add(tmp_usr)

            info_follow = []
            info_followed = []
            info_movie = {}
            info_book = {}

            url_follow = url['follow']+tmp_usr+'/contacts'
            url_followed = url['follow']+tmp_usr+'/rev_contacts'
            url_movie = url['movie']+tmp_usr+'/collect'
            url_book = url['book']+tmp_usr+'/collect'

            # 处理关注者
            cookie, header = SelectCookie()
            #header = {}

            follow_crawler(url_follow, info_follow, cookie, header, usr, dict_id_name,tmp_usr)


            #处理被关注者
            cookie, header = SelectCookie()
            follow_crawler(url_followed, info_followed, cookie, header, usr, dict_id_name)

            #处理看过的图书及其评分
            cookie, header = SelectCookie()
            book_list = []
            book_crawler(url_book, cookie, header, visited_book, book_list)

            #处理看过的电影及其评分
            cookie, header = SelectCookie()
            movie_list = []
            movie_crawler(url_movie, cookie, header, visited_movie, movie_list)

            usr_info = {'id': tmp_usr, 'name': dict_id_name[tmp_usr], 'follow': info_follow, 'followed': info_followed, 'movie': movie_list, 'book': book_list}
            usr_json = json.dumps(usr_info, ensure_ascii=False)
            fout.write(usr_json+'\n')
            fout.close()

            fout = codecs.open('usr_info.txt', 'a', 'utf_8_sig')
            print "local:", len(info_follow), len(info_followed), len(book_list), len(movie_list)
            print "total:", len(visited_user), len(visited_movie), len(visited_book)


def yudu():
    f = codecs.open('usr_info.txt', 'r', encoding='utf-8')

    allUsr = set()
    for x in f.readlines():
        #x = x.encode('utf-8')
        x= x[1:]
        tmp = json.loads(x)
        visited_user.add(tmp['id'])
        for y in tmp['follow']:
            allUsr.add(y)
        for y in tmp['followed']:
            allUsr.add(y)
        for y in tmp['movie']:
            visited_movie.add(y['id'])
        for y in tmp['book']:
            visited_book.add(y['id'])

    for x in allUsr:
        if x not in visited_user:
            usr.put(x)
    f.close()
    print '预处理完毕'
    print len(visited_user),usr._qsize(),len(visited_book),len(visited_movie)


if __name__=="__main__":
    yudu()
    crawler()        



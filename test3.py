#-*-coding:utf-8-*- #编码声明，不要忘记！
import random

import re
import requests  #这里使用requests，小脚本用它最合适！

import codecs
import Queue
import json

import time

import winsound
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
'll="118251"; bid=DeWGaaXkNVQ; ps=y; __yadk_uid=Zkwqg9xJGcAA6SfPyTwOUexmjX5EjtRp; push_noty_num=0; push_doumail_num=0; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1519231418%2C%22https%3A%2F%2Faccounts.douban.com%2Fsafety%2Funlock_sms%2Fresetpassword%3Fconfirmation%3Db070fdcd23be3708%26alias%3D%22%5D; _pk_ses.100001.8cb4=*; dbcl2="173611196:1rgP9WH9+DA"; ck=XuI5; _pk_id.100001.8cb4=f2443ab5bc95ec1d.1519209920.4.1519231436.1519223066.'
]
headers = [
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'},
    {
        'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; Touch; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; Tablet PC 2.0)'}
]
def get_proxies():
    page = requests.get('http://api.ip.data5u.com/dynamic/get.html?order=61ea3a0c5266d395453adee78637dfe4&sep=3')
    tree = html.fromstring(page.text)
    ip_port = tree.text.strip()
    return {'http': ip_port, 'https': ip_port}
    #return {}



def pause():
    time.sleep(5+5*random.random())
    return


def fobbiden_check(tree, original_url, session):
    title_name = tree.xpath('head/title/text()')
    while title_name[0] == u'403 Forbidden':
        print '403 Forbidden'
        proxies = get_proxies()
        page_follow = session.get(original_url, proxies=proxies)



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


def follow_crawler(url, info_follow, session,  usr_queue, dict_id_name, tmp_usr = ""):
    if url[0] == '/':
        url = main_url+url
    print url
    try:
        #proxies = {"http": "182.103.247.207:808", "https": "182.103.247.207:808" }
        #page_follow = requests.get(url, cookies=cookie, proxies=proxies)
        #hea = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}

        #page_follow = requests.get(url, cookies=cookie, proxies=proxies)
        page_follow = session.get(url, timeout=10)
        tree = html.fromstring(page_follow.text)
        print tree.xpath('head/title/text()')[0].strip()
        if tree.xpath('head/title/text()')[0].strip() == u'登录豆瓣':
            winsound.Beep(600, 10000)

        if tmp_usr != "":
            dict_id_name[tmp_usr] = tree.xpath('head/title/text()')[0].strip()[:-4]

        fobbiden_check(tree, url, session)
        intro_raw = tree.xpath('//dl[@class="obu"]/dd/a')
        #print tree.xpath('head/title/text()')[0]
    except:
        print '页面获取失败，正在重新获取代理ip'
        session.proxies = get_proxies()
        return url


    count_string = tree.xpath('//div[@class="info"]/h1/text()')[0]
    count_number = int(re.findall(r"\d+\.?\d*", count_string)[-1])
    print "关注数量有",count_number

    if count_number >10000:
        return 'error'

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
        return info_next[0]
    else:
        return ''

    
def book_crawler(url, session, visited_book, book_list):
    if url[0] == '/':
        url = main_url+url
    print url
    try:
        page_book = session.get(url, timeout=10)
        tree = html.fromstring(page_book.text)
        fobbiden_check(tree, url, session)

        #intro_raw = tree.xpath('//li[@class="subject-item"]/div[@class="info"]')
        intro_raw = tree.xpath('//li[@class="item"]/div[@class="item-show"]')

    except:
        print '页面获取失败，正在重新获取代理ip'
        session.proxies = get_proxies()
        return url

    for x in intro_raw:
        tmp_book_id = x.xpath('div[@class = "title"]/a/@href')[0].split('/')[4]

        book_title = x.xpath('div[@class = "title"]/a/text()')[0].strip()
        #rating = x.xpath('div[@class="short-note"]/div/span/@class')[0]
        rating = x.xpath('div[@class="date"]/span/@class')
        if len(rating) == 0:
            continue
        rating = rating[0]
        #print book_title

        if rating[0] == 'r':
            #print x.xpath('h2/a/@title')[0]
            date = x.xpath('div[@class="date"]/text()')[1].strip()
            rating = int(rating[6])
            visited_book.add(tmp_book_id)

            info_item = {'id': tmp_book_id, 'name': book_title, 'rating': rating, 'date': date}
            book_list += [info_item]


    info_next = tree.xpath('//div[@class="paginator"]/span[@class="next"]/link/@href')
    if len(info_next) == 1:
        pause()
        return info_next[0]
    else:
        return ''

def movie_crawler(url,session, visited_movie, movie_list):
    if url[0] == '/':
        url = main_url+url
    print url
    try:
        page_movie = session.get(url, timeout=10)
        tree = html.fromstring(page_movie.text)
        fobbiden_check(tree, url, session)
        intro_raw = tree.xpath('//li[@class="item"]/div[@class="item-show"]')
    except:
        print '页面获取失败，正在重新获取代理ip'
        session.proxies = get_proxies()
        return url


    for x in intro_raw:
        #print x.text
        #print x.xpath('ul/li[@class="title"]/a/@href')

        tmp_movie_id = x.xpath('div[@class = "title"]/a/@href')[0].split('/')[4]

        movie_title = x.xpath('div[@class = "title"]/a/text()')[0].strip()
        # rating = x.xpath('div[@class="short-note"]/div/span/@class')[0]
        rating = x.xpath('div[@class="date"]/span/@class')
        if len(rating) == 0:
            continue
        rating = rating[0]
        if rating[0] == 'r':
            #print x.xpath('h2/a/@title')[0]
            date = x.xpath('div[@class="date"]/text()')[1].strip()
            rating = int(rating[6])
            visited_movie.add(tmp_movie_id)
            #print date
            info_item = {'id': tmp_movie_id, 'name': movie_title, 'rating': rating, 'date': date}
            #print info_item
            movie_list+= [info_item]


    info_next = tree.xpath('//div[@class="paginator"]/span[@class="next"]/link/@href')
    if len(info_next) == 1:
        pause()
        return info_next[0]
    else:
        return ''

def SelectCookie():
    cookies = raw_cookies[0]
    cookie= {}
    for line in cookies.split(';'):
        key, value = line.split("=", 1)
        cookie[key] = value #一些格式化操作，用来装载cookies
    return cookie, headers[0]

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
    session = requests.Session()
    cookie, header = SelectCookie()
    #session.get('https://www.douban.com/people/171996611/contacts', cookies=cookie, headers = header)
    cookie_jar = requests.utils.cookiejar_from_dict(cookie, cookiejar=None, overwrite=True)
    session.cookies = cookie_jar
    session.headers['User-Agent'] = header['User-Agent']
    session.proxies = get_proxies()
    while not usr.empty():
        print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        tmp_usr = usr.get()
        if tmp_usr not in visited_user:
            print tmp_usr
            visited_user.add(tmp_usr)

            info_follow = []
            info_followed = []
            book_list = []
            movie_list = []
            info_movie = {}
            info_book = {}

            url_follow = url['follow']+tmp_usr+'/contacts'
            url_followed = url['follow']+tmp_usr+'/rev_contacts'
            url_movie = url['movie']+tmp_usr+'/collect'+'?sort=time&start=0&filter=all&mode=list&tags_sort=count'
            url_book = url['book']+tmp_usr+'/collect'+'?sort=time&start=0&filter=all&mode=list&tags_sort=count'

            try:
                # 处理关注者
                while url_follow != '':
                    cookie, header = SelectCookie()
                    #url_follow = follow_crawler(url_follow, info_follow, cookie, header, usr, dict_id_name,tmp_usr)
                    url_follow = follow_crawler(url_follow, info_follow, session, usr, dict_id_name, tmp_usr)
                if url_follow == 'error':
                    continue

                #处理被关注者
                while url_followed != '':
                    cookie, header = SelectCookie()
                    url_followed = follow_crawler(url_followed, info_followed, session,  usr, dict_id_name)
                if url_followed == 'error':
                    continue

                #处理看过的图书及其评分
                while url_book != '':
                    cookie, header = SelectCookie()
                    url_book = book_crawler(url_book, session,  visited_book, book_list)

                #处理看过的电影及其评分
                while url_movie != '':
                    cookie, header = SelectCookie()
                    url_movie = movie_crawler(url_movie, session,  visited_movie, movie_list)
            except:
                print '！！！！！！！！！！！出现异常！！！！！！！！！！'
                usr_info = {'id': tmp_usr, 'name': dict_id_name[tmp_usr]}
                if url_follow == '':
                    usr_info['follow'] = info_follow
                else:
                    print '抓取关注人员列表异常'

                if url_followed == '':
                    usr_info['follow'] = url_followed
                else:
                    print '抓取被关注人员列表异常'

                if url_book == '':
                    usr_info['book'] = url_book
                else:
                    print '抓取图书列表异常'

                if movie_list == '':
                    usr_info['movie'] = movie_list
                else:
                    print '抓取电影列表异常'
                usr_json = json.dumps(usr_info, ensure_ascii=False)
                fout_error = codecs.open('error_info.txt', 'a', 'utf_8_sig')
                fout_error.write(usr_json + '\n')
                fout_error.close()




            else:
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

    tmp_list = []
    for x in allUsr:
        if x not in visited_user:
            tmp_list.append(x)
    random.shuffle(tmp_list)
    for x in tmp_list:
        usr.put(x)
    f.close()
    print '预处理完毕'
    print len(visited_user),usr._qsize(),len(visited_book),len(visited_movie)


if __name__=="__main__":
    yudu()
    crawler()        



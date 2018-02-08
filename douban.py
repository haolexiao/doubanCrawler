# -*- coding: utf-8 -*-
from selenium import webdriver
import codecs
import Queue
import json
url = {'movie':'https://movie.douban.com/people/','book':'https://book.douban.com/people/','follow':'https://www.douban.com/people/'}

usr = Queue.Queue()
usr.put('luyazhang')
visited=set()
browser = webdriver.Chrome()
denglu = 'https://www.douban.com/accounts/login?redir=https%3A//www.douban.com/'
browser.get(denglu)



while not usr.empty():
    tmp_usr = usr.get();
    if tmp_usr not in visited:
        print tmp_usr
        tmp_follow = url['follow']+tmp_usr+'/contacts'
        tmp_followed = url['follow']+tmp_usr+'/rev_contacts'
        tmp_movie = url['movie']+tmp_usr+'/collect'
        tmp_book = url['book']+tmp_usr+'/collect'
        
    

file_output = codecs.open('thefile.csv','w', 'utf_8_sig')
for i in xrange(1,100):
    browser.get(url+str(i))
    List = browser.find_elements_by_xpath("//h3/a[@target='_blank']")
    for x in List:
        file_output.write(x.text+','+x.get_attribute('href'))
file_output.close()

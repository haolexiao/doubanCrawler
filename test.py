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
denglu = 'https://www.douban.com'
browser.get(denglu)


List = browser.find_element_by_xpath("//*[@id='email']")

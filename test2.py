
from selenium import webdriver
import re
import time
 
 
 
url = 'http://accounts.douban.com/login'
email = 'haolexiao'
password = 'plaxx692'
 
browser = webdriver.PhantomJS()
browser.get(url)

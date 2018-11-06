#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import codecs
#import json
#import random
import time
import traceback
#import urlparse
#import os
import traceback
import datetime

#import MySQLdb
#from pymongo import MongoClient
from lxml import etree
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

import qimai_config
import log_utils

log = log_utils.log_utils()


class QimaiQueryApi():
    def __init__(self):
        self.start_url = qimai_config.start_url

        self.firefox_options = webdriver.FirefoxOptions()
        self.firefox_options.set_headless()

        self.driver = webdriver.Firefox(firefox_options=self.firefox_options)
        self.driver.implicitly_wait(10)

    def __del__(self):
        self.driver.quit()


    def query(self, keywords, platForm):

        self.driver.get(qimai_config.query_url + '/' + keywords)
        
        '''
        s = '应用宝'
        x = s.decode('utf-8').encode('gbk')
        print(x)
        print("应用宝")
        '''

        ulDom = self.driver.find_element_by_xpath('//ul[@class="item-list"]')
        #ulDom = self.driver.find_element_by_css_selector('ul."item-list"')

        if platForm == 'yyb':
            platForm = '应用宝'
        elif platForm == 'bd':
            platForm = '百度'


        '''
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ivu-table-tbody')))
        except WebDriverException:
            print('out_of_time_while_search')
            return 'out_of_time_while_search'

        self.driver.find_element_by_link_text(platForm).click()
        '''


        # 等10秒页面加载完毕，然后选择对应平台
        for i in range(20):
            click_ok = False
            try:
                self.driver.find_element_by_link_text(platForm).click()
                click_ok = True
            except:
                time.sleep(0.5)
                if i >= 19:
                    log.info('out of time')

            if click_ok :
                break

        


        #time.sleep(5)
        body = self.driver.page_source
        page = etree.HTML(body)
        tr_list = page.xpath("//tbody[@class='ivu-table-tbody']/tr")

        cnt = 0
        tmpResll = []
        for tr in tr_list:
            appName = ''
            avator = ''
            rank = cnt
            company = ''
            infoUrl = ''

            cnt = cnt + 1

            td_list = tr.xpath("./td/div")

            try:
                rank = td_list[0].xpath("./span/text()")[0]
            except:
                pass
            
            td_list = tr.xpath("./td/div/div")

            try:
                infoUrl = td_list[0].xpath("./a/@href")[0]
            except:
                pass
            try:
                avator = td_list[0].xpath("./a/img/@src")[0]
            except:
                pass
            
            td_list = tr.xpath("./td/div/div/div")

            try:
                appName = td_list[0].xpath("./p/a/text()")[0]
            except:
                pass
            try:
                company = td_list[0].xpath("./p/text()")[0]
            except:
                pass

            tmpResll.append( [ appName, avator, rank, company, infoUrl] )
            

            #self.getInfo(td_list)

            if cnt >= 10:
                break


        #for x in tmpResll:
        #    print (x)

        self.handleTmpRes(tmpResll)

        return tmpResll
            
        #self.driver.find_element_by_xpath("")

    
    def getInfo(self, url):
        self.driver.get(url)
        #time.sleep(5)
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'app-info')))
        except WebDriverException:
            return 'out_of_time_while_search'
        body = self.driver.page_source
        page = etree.HTML(body)
        div = page.xpath('//div[@class="app-info"]/div[@class="appid"]')[0]
        bundle = ''
        try:
            bundle = div.xpath('./div/text()')[1]
        except:
            pass
        return bundle
        



    def handleTmpRes(self, tmpList):
        for app in tmpList:
            url = self.start_url + app[4]
            bundle = self.getInfo(url)
            #print bundle
            app[4] = bundle

            #print(app)
            #print(' ')


if __name__ == "__main__":
    q = QimaiQueryApi()

    start_time = time.time()
    q.query('初页','yyb')
    end_time = time.time()

    print(' ')
    print(start_time)
    print(end_time)

    
    #q = None

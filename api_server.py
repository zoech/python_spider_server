#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os   #Python的标准库中的os模块包含普遍的操作系统功能  
import re   #引入正则表达式对象  
import urllib   #用于对URL进行编解码
import json
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler  #导入HTTP处理相关的模块

from qimai_api import QimaiQueryApi


import sys 
reload(sys) 
sys.setdefaultencoding( 'utf-8')


SINGLEAPP = '{"appName":"%s","avator":"%s","rank":%s,"publisher":"%s","bundle":"%s"}'

RESPONSE = '{"rspCode":"%s","msg":"%s","data":%s}'



api = QimaiQueryApi()


#自定义处理程序，用于处理HTTP请求  
class TestHTTPHandler(BaseHTTPRequestHandler):

    #处理GET请求  
    def do_GET(self):
        #获取URL
        print 'URL=',self.path
        #页面输出模板字符串  
        templateStr = '''
        <html>   
        <head>   
        <title>QR Link Generator</title>   
        </head>   
        <body>   
        hello Python!
        </body>   
        </html>
        '''

        self.protocal_version = 'HTTP/1.1'  #设置协议版本  
        self.send_response(200) #设置响应状态码  
        self.send_header("Welcome", "Contect")  #设置响应头  
        self.end_headers()
        self.wfile.write(templateStr)   #输出响应内容


    def do_POST(self):
        length = int(self.headers.getheader('content-length'))
        qs = self.rfile.read(length)
        #url=urldecode(qs)
        print(qs)
        parms = json.loads(qs)
        print (parms['keyword'])
        print (parms['platform'])

        tmpList = []
        try:
            tmpList = api.query(parms['keyword'], parms['platform'])
        except:
            self.protocal_version = 'HTTP/1.1'
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            self.wfile.write(RESPONSE % ('00A0','服务器出错','null'))
            
            

        resList = []
        for app in tmpList:
            data = SINGLEAPP % (app[0], app[1], app[2], app[3], app[4])
            resList.append(data)

        res = '[' + ','.join(resList) + ']'


        self.protocal_version = 'HTTP/1.1'
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        self.wfile.write( RESPONSE % ('0000','success',res) ) 
        
        

        #启动服务函数  
def start_server(port):
        http_server = HTTPServer(('', int(port)), TestHTTPHandler)
        http_server.serve_forever() #设置一直监听并接收请求  

#os.chdir('static')  #改变工作目录到 static 目录


if __name__ == '__main__':
    start_server(9820)  #启动服务，监听8000端口

import requests
import json
import pandas as pd
from multiprocessing.dummy import Pool
import os
import time
import random

class mult_process():
    def __init__(self,domains):
        self.domains=domains
        self.error=[] #保存错误结果
        self.threads = 32
        self.count=0
    '''
    def get_json_data(self,domain): # 获取单个网站的product.json
        url = str('https://')+str(domain)+ '/products.json'
        page=1
        temp=[]
        for i in range(1,10):
            newurl=url+'?page='+str(page)
            try:
                webdata = requests.get(newurl,timeout=5).text
            except:
                pass
            else:
                temp.append(webdata)
            time.sleep(random.randint(1,5))
        print(self.count)
        self.count+=1

    '''
    def get_json_data(self,domain): # 获取单个网站的product.json
        url = str('https://')+str(domain)+ '/products.json'
        page=1
        temp=[]
        error_time=5 #设置五次差错
        while True:
            newurl=url+'?page='+str(page)
            if error_time==0:
                break
            try:
                webdata = requests.get(newurl,timeout=5).text
            except:
                error_time-=1
            else:
                if 'id' not in str(webdata):
                    break
                temp.append(webdata)
            page+=1
            print(page)
            time.sleep(random.randint(1,5))
        print(self.count)
        self.count+=1
        self.savetotxt(domain,data=temp)
        print(len(temp))

    '''
    def test_url(self,url):
        try:
            print(self.count)
            self.count+=1
            requests.get(newurl,timeout=5).text
        except:
            self.error.append(url)
            return False
        else:
            return True
    
    def down_one_shop_page(self,url,page):
        newurl=url+'?page='+str(page)
        try:
            webdata = requests.get(newurl,timeout=5).text
        except:
            return page  #返回出错的页面号
        else:
            if str(webdata)=='{"products":[]}': #终止页面
                return -1
            else:
                return webdata #返回数据

    def get_json_data(self,domain): # 获取单个网站的product.json
        url = str('https://')+str(domain)+ '/products.json'
        flag=self.test_url(url)
        error_page=[]
        temp=[]
        if flag==True: #如果能通过连接测试
            page=1 
            while True:
                webdata = self.down_one_shop_page(url,page)
                if webdata==-1:
                    break
                elif type(webdata)==str:
                    temp.append(webdata)
                else:
                    error_page.append(webdata)
                page+=1
        # Try again 
        if len(error_page)!=0:
            for item in error_page:
                webdata=self.down_one_shop_page(url,item)
                if type(webdata)==str:
                    temp.append(webdata)
        self.savetotxt(domain,data=temp)
        print(len(temp))

        error_page=[]
        temp=[]
        count=1
        #cmpdata=''
        while True:
            newurl=url+'?page='+str(count)
            try:
                webdata = requests.get(newurl,timeout=5).text
                
                # try 1
                if str(webdata)!=cmpdata:
                    cmpdata=webdata
                else:
                    break
                # try 2
                #{"products":[]}
                if str(webdata)=='{"products":[]}': # unknown error 
                    break
                # try 3
                if 'id' not in webdata:
                    break
                # try 4 modify except
                if str(webdata)=='{"products":[]}': 
                    break
            except:
                error_page.append(count)
                break
            else:
                temp.append(webdata)
                count+=1
    '''

    def savetotxt(self,domain,data):
        f=open('jsonres/'+domain+'.json.txt','w',encoding='utf-8')
        for i in data:
            f.write(i)
            f.write('\n')
        f.close()


    def multiply_process(self):
        pool = Pool(self.threads)
        pool.map(self.processForMul,range(self.threads))
        pool.close()
        pool.join()

    def process(self,domain):
        try:
            self.get_json_data(domain)
        except:
            print(domain +' : ERROR')

    def processForMul(self,threads):
        for i in range(threads,len(self.domains),self.threads):
            self.process(self.domains[i])

    def handleError(self):
        f=open('wrong.txt','w',encoding='utf-8')
        for i in self.error:
            f.write(i)
            f.write('\n')
        f.close()




if __name__ == "__main__":
    lst=['www.nativeunion.com','www.colourpop.com']
    #lst=
    s=mult_process(lst)
    s.multiply_process()
    s.handleError()


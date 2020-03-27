import requests
import json
import pandas as pd
from multiprocessing.dummy import Pool
import os
import time
import random
from fake_useragent import UserAgent
from pyquery import PyQuery as pq
import re
from shop_data_mining import SHOP

class DataAnalysis():

    # init
    def __init__(self,domain):
        self.domain=domain #域名
        self.valid=True #默认可以访问
        self.products_num_in_xml=0 #xml中产品数量
        self.get_json_flag=False # 获取json中是否出错
        
        self.shop_num=0 #验证后的产品数量
        self.socialurls=[] # 社交账号
        self.sitemap=[] # sitemap中所有链接
        self.res=[] # 所有json数据

        self.fileinit()

    def fileinit(self):
        with open('./'+self.domain+'/attr.txt','r',encoding='utf-8') as f:
            lst=f.read().split('\n')
            self.valid=bool(lst[1])
            self.products_num_in_xml=int(lst[2])
            self.get_json_flag=bool(lst[3])
    


    # func 
    def get_sitemap(self):
        with open('./'+self.domain+'/sitemap.txt','r',encoding='utf-8') as f:
            sitemap=f.read().split('\n')
            if len(sitemap)>=2:
                self.sitemap=sitemap[0:-1]
    
    def get_social_urls(self):
        with open('./'+self.domain+'/index.txt','r',encoding='utf-8') as f:
            content=f.read()
        if content!='':
            page=pq(content,parser="html")
            lst=page('a').items()
            for i in lst:
                temp=i.attr('href')
                if temp!=None and self.domain not in temp and '://' in temp : 
                   self.socialurls.append(temp)
    
    def parse_json(self):

        os.chdir(self.domain)
        content=self.readfile(self.domain+'.json.txt')
        handle=[]
        if content!=[]:
            handle=[]
            for i in range(len(content)-1):
                jsondata=json.loads(content[i])['products']
                for item in jsondata:
                    self.res.append(item)
                    handle.append(item['handle'])
            print(len(handle))
            if self.get_json_flag==True or len(handle)!=self.products_num_in_xml:
                self.res.extend(self.shop_validation(handle=handle))
            os.chdir('..')
        
        self.shop_num=len(self.res)
        self.writetotxt(self.domain+'.data.txt',self.res)


    #Tools 
    def shop_validation(self,handle): # compare  between the handles and the urls in xml 
        res=[]
        with open(self.domain+'.xml.txt') as f:
            content=f.read().split('\n')
            if len(content)>=2:
                for i in range(1,len(content)-1):
                    temp=content[i].split('/')
                    if len(temp)>0 and temp[-1] not in handle:
                        res.append(self.get_json_data(productname=temp))
        return res


    def get_json_data(self,productname): # 获取单个商品的json

        url = r'https://' + str(self.domain) + '/products/' + str(productname) + '.js'
        try:
            webdata = requests.get(url).text
            data = json.loads(webdata)
        except:
            pass
        else:
           return str(data)

    def writetotxt(self,filename,data):
        if type(data)==list and len(data)!=0:
            f=open(filename,'w',encoding='utf-8')
            for i in data:
                f.write(str(i))
                f.write('\n')
            f.close()


    def readfile(self,filename):
        f=open(filename,'r',encoding='utf-8')
        content=f.read().split('\n')
        return content

    
    # run
    def run(self):
        self.get_sitemap()
        self.get_social_urls()
        self.parse_json()
        print(self.socialurls)
        print(self.sitemap)
        print(self.shop_num)



if __name__ == "__main__":
    lst=open('data.txt').read().split('\n')[0:10]
    for i in lst:
        try:
            shop=SHOP(i)
            shop.run()
            da=DataAnalysis(i)
            da.run()
        except:
            print(i+':wrong!')

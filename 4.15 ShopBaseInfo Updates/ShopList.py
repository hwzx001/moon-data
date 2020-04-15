'''
Name    : Collections Of Shopifies Stores Data 
Version : 0.1.6
Updates Time: 2020.04.15
Author  : Lucky 
Update Content ：
    04.09
    1、modify：
        fun getIndexPageTitleANDShopSocail --parse the html with pyquery library 

    2、modify: 
        fun getProductUrl   --some products url more than one page
            Ex : https://beckettsmusic.co.uk/sitemap.xml
            p1: https://beckettsmusic.co.uk/sitemap_products_1.xml?from=452041998378&to=1926660194346
            p2: https://beckettsmusic.co.uk/sitemap_products_2.xml?from=1928970272810&to=4526147895375

    3、add   : 
        class multiRecord   --added concurrent processing of processes; 
    
    4、delete：
        class addRecord

    5、Need To Do：
        modify the 'ShopNumofProducts' through json content  --Some companies have hidden product pages
                Ex https://alohagolfcenter.net/sitemap.xml

    04.15
    1、modfiy
        class ShopInfoRecord -- added function timeout mechanism
        
    2、add
        fun getCreatedAt
        fun getIndexPageTitleANDShopSocailANDCurrency

    3、modfiy
        class multiRecord -- Added function timeout mechanism
'''

import re 
import requests 
import os
import pymysql 
import pymysql.cursors
from fake_useragent import UserAgent
from pyquery import PyQuery as pq 
from multiprocessing.dummy import Pool,Lock
import xmltodict as xd 
import json
from pprint import pprint
from datetime import datetime
import math
import time 
import random
import eventlet
import time


# global varients 
ua=UserAgent(verify_ssl=False)
headers={"User-Agent": ua.chrome}	
social_keys=['amazon',  'businessinsider', 'citiesocial', 'cyrillcase', 'decathlon-united', 'facebook',  'instagram',  'livechatinc', 'mailchi', 'pinterest', 'reddit', 'reddress', 'shopperapproved', 'snapchat', 'spigen', 'stevemadden', 'tiktok', 'twitter', 'vimeo', 'wsj', 'youtube']
lock=Lock()


class ShopInfoRecord():

    def __init__(self,URL):
        self.url = URL
        self.IsValid= 1
        self.ShopIndexPageTitle = 'NULL'	
        self.ShopCountry = 'Unknown'
        self.ShopSocail = {}
        self.ShopCreated = 'NULL'
        self.Categories='NULL'
        self.Currency='NULL'
        self.Technologies='Unknown'

        self.ShopNumofProducts=0
        

    # funs 
    def getIndexPageTitleANDShopSocailANDCurrency(self):
        rawtext = self.getWebPage(r'https://'+self.url)
        if rawtext == '':
            self.IsValid = 0
        else:
            #title 
            page = pq(rawtext,parser="html")
            try:
                self.ShopIndexPageTitle=page('title').text()
            except:
                pat = re.compile(r'<title>([\s\S]+)</title>')
                s = re.search(pat,rawtext)
                if s != None:
                    temp=str(s.group(1).strip())
                    if len(temp)>=255:
                        title=temp.split('\n')[0].strip()
                        self.ShopIndexPageTitle=title
                    else:
                        self.ShopIndexPageTitle=temp 

            # social 
            lst = page('a').items()
            for i in lst:
                temp = i.attr('href')
                if temp != None: 
                    for j in social_keys:
                        if j in temp:
                            self.ShopSocail[str(j)] = temp
                    
            # currency
            currency=self.find_currency(rawtext)
            if currency!='NULL':
                dict_cur=eval(currency)
                if 'active' in dict_cur.keys():
                    self.Currency=dict_cur['active']
                else:
                    self.Currency=currency



    def getNumofProducts(self):
        productUrl=self.getProductUrl()
        if len(productUrl)!=0:
            count=0
            for i in productUrl:
                rawtext = self.getWebPage(i)
                data=self.parsexml(rawtext)
                if 'urlset' in data.keys() and 'url' in data['urlset'].keys():
                    count+=len(data['urlset']['url'])-1 #remove the first domain
                else:
                    count+=len(self.reparse(rawtext))-1
            self.ShopNumofProducts=count
        else:
            self.ShopNumofProducts=0


    def getProductUrl(self):
        rawtext = self.getWebPage(r'https://'+self.url+r'/sitemap.xml')
        lst=self.reparse(rawtext)
        res=[]
        if len(lst)!=0:
            for i in lst:
                if 'product' in i and 'https:' in i and 'cdn' not in i:
                    res.append(i) 
        return res 
    
    def getCreatedAt(self):
        pages=math.ceil(self.ShopNumofProducts/30)
        urlpat=r'https://'+self.url+r'/products.json?page='
        tempres=[]
        for i in range(1,pages+1):
            try:
                rawtext = self.getWebPage(urlpat+str(i))
                tempres.append(self.find_created_at(rawtext))
            except Exception as e:
                print(e)

        if len(tempres)!=0:
            self.ShopCreated=str(min(tempres))[0:10]
            #time.sleep(random.randint(2,5))
        else:
            self.ShopCreated='2099-12-31'
            


    #TOOLS

    def find_created_at(self,data):
        res=[]
        try:
            jsondata=json.loads(data)['products']
            for item in jsondata:
                cmpdat=item['created_at']
                res.append(cmpdat)      
        except Exception as e:
                print(e)
        if len(res)!=0:
            return min(res)
        else:
            return '2099-12-31'


    def find_currency(self,string):
        pat=re.compile(r'Shopify.currency = (\{[\s\S]+?\})')
        s=re.search(pat,string)
        if s!=None:
            return s.group(1)
        return 'NULL'

    def parsexml(self,data):
        return json.loads(json.dumps(xd.parse(data),indent=1))
    
    
    def reparse(self,string):
        pat=re.compile(r'\>(.*?)\<')
        s=re.findall(pat,string)
        res=[]
        for i in s:
            if i!='' and 'https'in i  and 'cdn'not in i:
                res.append(i)
        return res 
    
    def getWebPage(self,links):
        try:
            page = requests.get(links,headers=headers,timeout=10).text
        except:
            return ''
        else:
            return page
    
    # run
    def run(self):
        eventlet.monkey_patch()
        with eventlet.Timeout(60,False):
            self.getIndexPageTitleANDShopSocailANDCurrency()
            if self.IsValid!=0:
                self.getNumofProducts()
                self.getCreatedAt()
            return (
                    self.url,
                    self.IsValid,
                    self.ShopIndexPageTitle,	
                    self.ShopCountry,
                    str(self.ShopSocail),
                    self.ShopCreated ,
                    self.Categories,
                    self.Currency,
                    self.Technologies
                    )





class multiRecord():
    def __init__(self):
        Date=datetime.now().strftime('%Y-%m-%d')
        self.f=open('ShopListRecord'+str(Date)+'.txt','w',encoding='utf-8')
        self.data=open('res.txt').read().split('\n')[0:200]
        #multiprocess
        self.threads = 512
        self.count=0
    
    def __del__(self):
        self.f.close()

    def multiply_process(self):
        pool = Pool(self.threads)
        pool.map(self.processForMul,range(self.threads))
        pool.close()
        pool.join()
    
    def processForMul(self,threads):
        for i in range(threads,len(self.data),self.threads):
            self.process(self.data[i])
    
    def process(self,url):
        eventlet.monkey_patch()
        with eventlet.Timeout(45,False):
            try:
                self.get_data(url=url)
            except Exception as e:
                print(e)   
            
    
    def get_data(self,url):
        try:
            shopinf = ShopInfoRecord(url)
            data=shopinf.run()
        except Exception as e :
            print(e)
        else:
            lock.acquire()
            self.f.write(str(data))
            self.f.write('\n')
            lock.release()
        finally:
            print(self.count)
            self.count+=1
    
    def run(self):
        self.multiply_process() 

    
if __name__ == "__main__":
   
   a=multiRecord()
   a.run()

'''
Name    : Collections Of Shopifies Stores Data 
Version : 0.1.2
Updates Time: 2020.04.09
Author  : Lucky 
Update Content ：
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


# global varients 
ua=UserAgent(verify_ssl=False)
headers={"User-Agent": ua.chrome}	
social_keys=['amazon',  'businessinsider', 'citiesocial', 'cyrillcase', 'decathlon-united', 'facebook',  'instagram',  'livechatinc', 'mailchi', 'pinterest', 'reddit', 'reddress', 'shopperapproved', 'snapchat', 'spigen', 'stevemadden', 'tiktok', 'twitter', 'vimeo', 'wsj', 'youtube']
lock=Lock()

# get records(id,url) from table 'DomainList' 
def readDomainList():
    connection=pymysql.connect(
                                        host="35.224.151.74", #ip
                                        user="root",# usr name
                                        password="", #pwd
                                        db="DomainDB", # db name
                                        charset='utf8'
                                        )
    cs=connection.cursor()
    sql='''SELECT `ID`,`URL` FROM `DomainList` WHERE IsValid='1';'''
    cs.execute(sql)
    data=cs.fetchall() 
    cs.close()
    connection.close()
    return data



class ShopInfoRecord():

    def __init__(self,ID,URL):
        self.ID = ID
        self.url = URL
        self.ShopIndexPageTitle = ''	
        self.ShopNumofProducts = 0 
        self.ShopMonthlyTraffic = 0 #月流量 
        self.ShopSocail = {}
        self.ShopAveragePriceUSD = 0.0
        self.ShopType = 'Shopify'	
        self.ShopCountry = 'Unknown'

    # funs 
    def getIndexPageTitleANDShopSocail(self):
        rawtext = self.getWebPage(r'https://'+self.url)

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
                        self.ShopSocail[str(j)] = {
                            "url" :temp,
                            "nums":0
                        }

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

    #TOOLS
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
        self.getIndexPageTitleANDShopSocail()
        self.getNumofProducts()
        return (
                self.ID,
                self.url,
                self.ShopIndexPageTitle ,	
                self.ShopNumofProducts ,
                self.ShopMonthlyTraffic,
                str(self.ShopSocail) ,
                self.ShopAveragePriceUSD ,
                self.ShopType,	
                self.ShopCountry)





class multiRecord():
    def __init__(self):
        Date=datetime.now().strftime('%Y-%m-%d')
        self.f=open('ShopListRecord'+str(Date)+'.txt','w',encoding='utf-8')
        self.data=readDomainList()
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
    
    def process(self,tupleRecord):
        try:
            self.get_data(tupleRecord=tupleRecord)
        except Exception as e:
            print(tupleRecord)
            print(e)   
           
    
    def get_data(self,tupleRecord):
        temp_id=tupleRecord[0]
        temp_url=tupleRecord[1]
        try:
            temp=self.getRecord(temp_id,temp_url)
        except Exception as e :
            print(e)
        else:
            lock.acquire()
            self.f.write(str(temp))
            self.f.write('\n')
            lock.release()
        finally:
            print(self.count)
            self.count+=1


    
    def run(self):
        self.multiply_process() 
       
    
    def getRecord(self,id,url):
        shopinf = ShopInfoRecord(id,url)
        data=shopinf.run()
        return data 
    

    


if __name__ == "__main__":
   
    m=multiRecord()
    m.run()
   
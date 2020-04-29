import re 
import requests 
from pyquery import PyQuery as pq  
from fake_useragent import UserAgent
import xmltodict as xd 
import json
import math
import time 
import random
import numpy as np
from scipy import stats
import eventlet
from datetime import datetime
from multiprocessing.dummy import Pool,Lock
import pymysql 
import pymysql.cursors

ua=UserAgent(verify_ssl=False)
headers={"User-Agent": ua.chrome}
lock=Lock()
def getmyurl(url):
    try:
        #headers=headers,timeout=10
        page = requests.get(url=url,timeout=10).text
    except Exception as e:
        return str(e)
    else:
        return str(page) 

def getWeb(url):
    #https://us-central1-project-moon-271201.cloudfunctions.net/function-test?message=
    temp='https://us-central1-project-moon-271201.cloudfunctions.net/function-test?message='+str(url)
    return getmyurl(temp)
# get shop all json

def getIdandURL(nums):
    try:
        connection=pymysql.connect(
                                            host="35.224.151.74", #ip
                                            user="root",# usr name
                                            password="", #pwd
                                            db="DomainDB", # db name
                                            charset='utf8'
                                            )
        cs=connection.cursor()
        sql='SELECT `No`,`URL` FROM ShopBaseInfo LIMIT '+str(nums)
        cs.execute(sql)
        data=cs.fetchall()
    except Exception as e:
        print(e)
    else:
        cs.close()
        connection.close()
        return data

class multiJson():
    def __init__(self,URL):
        self.url = URL
        self.ShopNumofProducts=0
        #multiprocess
        self.threads = 100
        self.count=0
        self.urlpat=r'https://'+URL+r'/products.json?page='
        self.data=[]
        self.res=[]
        self.error=[]
    

    def multiply_process(self):
        pool = Pool(self.threads)
        pool.map(self.processForMul,range(self.threads))
        pool.close()
        pool.join()
    
    def processForMul(self,threads):
        for i in range(threads,len(self.data),self.threads):
            self.process(self.data[i])
    
    def process(self,url):
        try:
            self.get_data(url=url)
        except Exception as e:
            print(e)   
        
    
    def get_data(self,url):
        try:
            data=self.getjsondata(url)
        except Exception as e :
            self.error.append(url)
            print(e)
        else:
            lock.acquire()
            if data!='':
                self.res.extend(data)
            else:
                self.error.append(url)
            lock.release()
        finally:
            #print(self.count)
            self.count+=1
      
    
    def geturl(self):
        pages=math.ceil(self.ShopNumofProducts/30)
        for i in range(1,pages+1):
            self.data.append(self.urlpat+str(i))

    def getjsondata(self,url):
            try:
                rawtext = getWeb(url)
            except Exception as e:
                print(e)
                return ''
            else:
                if rawtext!='':
                    data=self.parseRecord(rawtext)
                return data

    def parseRecord(self,rawtext):
        data=json.loads(rawtext)
        if 'products'in data.keys():
            temp=data['products']
            if temp!='':
                return temp
    
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
        if self.ShopNumofProducts >99999: #超过10w的商家暂时不考虑
            self.ShopNumofProducts=99999
    
    def getProductUrl(self):
        rawtext = self.getWebPage(r'https://'+self.url+r'/sitemap.xml')
        lst=self.reparse(rawtext)
        res=[]
        if len(lst)!=0:
            for i in lst:
                if 'product' in i and 'https:' in i and 'cdn' not in i:
                    res.append(i)
        return res 
    
    
    def getWebPage(self,links):
        try:
            page = requests.get(links,headers=headers,timeout=10).text
        except Exception as e:
            print(e)
            return ''
        else:
            return page
    
    def getjsondataOfError(self,url):
            try:
                rawtext = self.getWebPage(url)
            except Exception as e:
                print(e)
                return ''
            else:
                if rawtext!='':
                    data=self.parseRecord(rawtext)
                return data

    '''
    def getWeb(self,links):
        temp=getmyurl('https://us-central1-project-moon-271201.cloudfunctions.net/function-test?message='+str(links))
        print(temp)
        if 'HTTPSConnectionPool'not in temp :
            return temp
        else:
            return ''
    '''

    def reparse(self,string):
        pat=re.compile(r'\>(.*?)\<')
        s=re.findall(pat,string)
        res=[]
        for i in s:
            if i!='' and 'https'in i  and 'cdn'not in i:
                res.append(i)
        return res 
    
    def parsexml(self,data):
        return json.loads(json.dumps(xd.parse(data),indent=1))
    
    ''' error and run '''
    def errorHandling(self):
        if len(self.error)!=0:
            for i in self.error:
                try:
                    data=self.getjsondata(i)
                except Exception as e :
                    print(e)
                else:
                    if data!='':
                        self.res.extend(data)

    def run(self):
        self.getNumofProducts()
        self.geturl()
        self.multiply_process()
        self.errorHandling()
        if len(self.res)!=0:
            return self.res 
        else:
            return []

class analysisOfProduct():
    def __init__(self,URL):
        self.url = URL
        self.jsondata=[]
        self.ShopNumofProducts=0
        self.isValid=True

        self.maxPrice=0.0
        self.minPrice=0.0
        self.avgPrice=0.0
        self.diffPrice=0
        self.midPrice=0.0 # mid
        self.modePrice=0.0 # mode 

        self.vendor=[]
        self.lastCreatedAt=""
        self.lastPusblishedAt=""
        self.lastUpdateAt=""
        self.oldPublishedAt=""
        self.produType=[]

        

    # Record:
    #['id', 'title', 'handle', 'body_html', 'published_at', 
    # 'created_at', 'updated_at', 'vendor', 'product_type', 
    # 'tags', 'variants', 'images', 'options']

    # variants
    #['id', 'title', 'option1', 'option2', 'option3', 
    # 'sku', 'requires_shipping', 'taxable', 'featured_image', 'available', 'price', 
    # 'grams', 'compare_at_price', 'position', 'product_id', 'created_at', 'updated_at']
    


    def analysisVariants(self):
        price=[]
        for item in self.jsondata:
            temp=item["variants"][0]
            price.append(float(temp['price']))
        self.maxPrice=max(price)
        self.minPrice=min(price)
        self.avgPrice=round(sum(price)/len(price),2)
        self.diffPrice=len(set(price))
        self.midPrice=np.median(price)
        self.modePrice=stats.mode(price)[0][0]
    
    def analysisDateAndVendor(self):
        publish=[]
        created=[]
        updated=[]
        for item in self.jsondata:
            tempvendor=item['vendor']
            if tempvendor not in self.vendor:
                self.vendor.append(tempvendor)
            produtype=item['product_type']
            if produtype!='' and produtype not in self.produType:
                self.produType.append(produtype)
            created.append(item['created_at'])
            updated.append(item['updated_at'])
            publish.append(item['published_at'])
        self.lastPusblishedAt=max(publish)
        self.lastCreatedAt=max(created)
        self.lastUpdateAt=max(updated)
        self.oldPublishedAt=min(publish)


   
    
    def getjsondata(self):
        temp=multiJson(self.url)
        res=temp.run()
        if len(res)!=0:
            self.ShopNumofProducts=len(res)
            self.jsondata=res
        else:
            self.isValid=False

    
    #tools 
    def parseRecord(self,rawtext):
        data=json.loads(rawtext)
        if 'products'in data.keys():
            temp=data['products']
            if temp!='':
                return temp

    def getWebPage(self,links):
        try:
            page = requests.get(links,headers=headers,timeout=10).text
        except Exception as e:
            print(e)
            return ''
        else:
            return page
    
    def reparse(self,string):
        pat=re.compile(r'\>(.*?)\<')
        s=re.findall(pat,string)
        res=[]
        for i in s:
            if i!='' and 'https'in i  and 'cdn'not in i:
                res.append(i)
        return res 
    
    def parsexml(self,data):
        return json.loads(json.dumps(xd.parse(data),indent=1))
    
    #run
    def run(self):
        try:
            self.getjsondata()
            self.analysisVariants()
            self.analysisDateAndVendor()
        except Exception as e:
            return str(e)
        else:
            if self.isValid==True:
                res={}
                res["url"]=self.url
                res["nums"] = self.ShopNumofProducts
                res['price'] = {}
                res['price']["maxPrice"] = self.maxPrice
                res['price']["minPrice"] = self.minPrice
                res['price']["avgPrice"] = self.avgPrice
                res['price']["diffPrice"] = self.diffPrice
                res['price']["midPrice"] = self.midPrice
                res['price']["modePrice"] = self.modePrice
                res["vendor"] = self.vendor
                res['date']={}
                res['date']["lastCreatedAt"] = self.lastCreatedAt
                res['date']["lastPublishedAt"] = self.lastPusblishedAt
                res['date']["lastUpdateAt"] = self.lastUpdateAt
                res['date']["oldPublishedAt"] = self.oldPublishedAt
                res['produType']=self.produType

                return res
            else:
                return ''


class getMultiRecord():
    def __init__(self):
        Date=datetime.now().strftime('%Y-%m-%d')
        self.f=open('ShopActiveInfo'+str(Date)+'.txt','w',encoding='utf-8')
        self.data=getIdandURL(500)
        #multiprocess
        self.threads = 50
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
    
    def process(self,record):
        try:
            self.get_data(id=record[0],url=record[1])
        except Exception as e:
            print(e)   
            
    
    def get_data(self,id,url):
        try:
            temp=analysisOfProduct(url)
            data=temp.run()
        except Exception as e :
            print(e)
        else:
            if data!='' and type(data)==dict:
                tempres={}
                tempres[id]=data
                lock.acquire()
                self.f.write(str(tempres))
                self.f.write('\n')
                lock.release()
        finally:
            print(self.count)
            self.count+=1
    
    def run(self):
        self.multiply_process() 


 

if __name__ == "__main__":
    s=getMultiRecord()
    s.run()

    

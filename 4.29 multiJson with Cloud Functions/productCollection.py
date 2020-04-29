from flask import Flask
from flask import request
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



app = Flask(__name__)
ua=UserAgent(verify_ssl=False)
headers={"User-Agent": ua.chrome}
lock=Lock()
pro=[]
#methods=['GET', 'POST']
@app.route('/api/<id>')
def home(id):
    if '.' not in str(id):
        return 'ERROR'
    else: 
        a=analysisOfProduct(id)
        res=a.run()
        return str(res)
#new products sort by created at date 10
#


class analysisOfProduct():
    def __init__(self,URL):
        self.url = URL
        self.jsondata=[]
        self.ShopNumofProducts=0

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

        self.bestSellGoods={}
        self.newProducts={}
        

    # Record:
    #['id', 'title', 'handle', 'body_html', 'published_at', 
    # 'created_at', 'updated_at', 'vendor', 'product_type', 
    # 'tags', 'variants', 'images', 'options']

    # variants
    #['id', 'title', 'option1', 'option2', 'option3', 
    # 'sku', 'requires_shipping', 'taxable', 'featured_image', 'available', 'price', 
    # 'grams', 'compare_at_price', 'position', 'product_id', 'created_at', 'updated_at']
    def getnewProducts(self):
        res=sorted(self.jsondata,key=lambda x: x['created_at'],reverse=True)
        if len(res)>7:
            for i in range(7):
                data=res[i]
                details={}
                try:
                    details['title']=data['title']
                    details['url']=self.url+'/'+data['handle']
                    details['created_at']=data['created_at']
                    details['price']=data['variants'][0]['price']
                    details['featured_image']=data['variants'][0]['featured_image']['src']
                except Exception as e:
                    print(1)
                    print(e)
                finally:
                    self.newProducts[i]=details
        elif len(res)>0:
            for i in range(len(res)):
                data=res[i]
                details={}
                try:
                    details['title']=data['title']
                    details['url']=self.url+data['handle']
                    details['created_at']=data['created_at']
                    details['price']=data['variants']['price']
                    details['featured_image']=data['variants']['featured_image']['src']
                except Exception as e:
                    print(2)
                    print(e)
                finally:
                    self.newProducts[i]=details


    def getbestSellGoods(self):
        url=r'https://'+self.url+r'/collections/all?sort_by=best-selling'
        rawtext=self.getWebPage(url)
        lst=pq(rawtext).items('a')
        res=[]
        for i in lst:
            temp=i.attr('href')
            if temp not in res:
                if str(temp).startswith('/collections/all/products/') or str(temp).startswith('/products/') :
                    res.append(temp)
            if len(res)>6:
                break
        if len(res)!=0:
            for i in range(len(res)):
                tempres={}
                links=r'https://'+self.url+res[i]
                details=self.getDetails(links)
                tempres['details']=details
                self.bestSellGoods[i]=tempres

    
    def getDetails(self,links):
        #['id', 'title', 'handle', 'description', 'published_at', 
        # 'created_at', 'vendor', 'type', 'tags', 'price', 'price_min', 
        # 'price_max', 'available', 'price_varies', 'compare_at_price', 'compare_at_price_min', 
        # 'compare_at_price_max', 'compare_at_price_varies', 'variants', 'images', 
        # 'featured_image', 'options', 'url', 'media']
        details={}
        rawtext=self.getWebPage(links+'.js')
        if rawtext!='':
            try:
                data=json.loads(rawtext)
                details['title']=data['title']
                details['url']=links
                details['published_at']=data['published_at']
                details['price']=data['price']
                details['price_min']=data['price_min']
                details['price_max']=data['price_max']
                details['featured_image']=data['featured_image']
            except Exception as e:
                print(3)
                print(e)
        return details
            

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
    
    def getjsondata(self):
        pages=math.ceil(self.ShopNumofProducts/30)
        urlpat=r'https://'+self.url+r'/products.json?page='
        for i in range(1,pages+1):
            try:
                rawtext = self.getWebPage(urlpat+str(i))
                self.jsondata.extend(self.parseRecord(rawtext))
            except Exception as e:
                print(4)
                print(e)
        self.ShopNumofProducts=len(self.jsondata)
    
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
        except:
            print(5)
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
            self.getNumofProducts()
            self.getjsondata()
            self.getnewProducts()
            self.getbestSellGoods()
            self.analysisVariants()
            self.analysisDateAndVendor()
        except Exception as e:
            print(6)
            return str(e)
        else:
            res={}
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
            res["produType"] = self.produType
            res['bestSell'] = self.bestSellGoods
            res['newProduct']=self.newProducts
            return res
        

class multiJson():
    def __init__(self,URL):
        self.url = URL
        self.ShopNumofProducts=0
        #multiprocess
        self.threads = 500
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
            lock.release()
        finally:
            print(self.count)
            self.count+=1
      
    
    def geturl(self):
        pages=math.ceil(self.ShopNumofProducts/30)
        for i in range(1,pages+1):
            self.data.append(self.urlpat+str(i))

    def getjsondata(self,url):
            try:
                print(url)
                rawtext = getweb(url)
                data=self.parseRecord(rawtext)
            except Exception as e:
                print(e)
                return ''
            else:
                print(rawtext)
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
        '''
        with open('test.txt','w',encoding='utf-8') as f:
            for i in self.res:
                f.write(str(i))
                f.write('\n')
        '''
        if len(self.res)!=0:
            return self.res 
        else:
            return []

def getmyurl(url):
    try:
        #headers=headers,timeout=10
        page = requests.get(url=url,timeout=10).text
    except Exception as e:
        return str(e)
    else:
        return str(page)

def getweb(url):
    return getmyurl('https://us-central1-project-moon-271201.cloudfunctions.net/function-test?message='+str(url))

if __name__ == '__main__':
    a=multiJson('colourpop.com')
    print(len(a.run()))
   
    

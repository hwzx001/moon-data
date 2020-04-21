from flask import Flask
from flask import request
import re 
import requests 
import pymysql 
import pymysql.cursors
from fake_useragent import UserAgent
import xmltodict as xd 
import json
import math
import time 
import random
import numpy as np
from scipy import stats


app = Flask(__name__)
ua=UserAgent(verify_ssl=False)
headers={"User-Agent": ua.chrome}

#methods=['GET', 'POST']
@app.route('/api/<id>')
def home(id):
    a=analysisOfProduct(id)
    res=a.run()
    print(res)
    return res 

class analysisOfProduct():
    def __init__(self,URL):
        self.url = URL
        self.jsondata=[]
        self.ShopNumofProducts=0

        self.maxPrice=0.0
        self.minPrice=0.0
        self.avgPrice=0.0
        self.diffPrice=0
        self.midPrice=0.0 # 中位数
        self.modePrice=0.0 #众数

        self.vendor=[]
        self.lastCreatedAt=""
        self.lastPusblishedAt=""
        self.lastUpdateAt=""
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
            self.analysisVariants()
            self.analysisDateAndVendor()
        except Exception as e:
            return str(e)
        else:
            res={}
            res["nums"] = self.ShopNumofProducts
            res["maxPrice"] = self.maxPrice
            res["minPrice"] = self.minPrice
            res["avgPrice"] = self.avgPrice
            res["diffPrice"] = self.diffPrice
            res["midPrice"] = self.midPrice
            res["modePrice"] = self.modePrice
            res["vendor"] = self.vendor
            res["lastCreatedAt"] = self.lastCreatedAt
            res["lastPublishedAt"] = self.lastPusblishedAt
            res["lastUpdateAt"] = self.lastUpdateAt
            res["produType"] = self.produType
            return res
        

        


if __name__ == '__main__':
    app.run(debug=True)
    

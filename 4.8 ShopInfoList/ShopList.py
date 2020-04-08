from multiprocessing.dummy import Pool
import re 
import requests 
import os
import pymysql 
import pymysql.cursors
from fake_useragent import UserAgent
from pyquery import PyQuery as pq 
import xmltodict as xd 
import json
from pprint import pprint

ua=UserAgent(verify_ssl=False)
headers={"User-Agent": ua.chrome}	
social_keys=['amazon',  'businessinsider', 'citiesocial', 'cyrillcase', 'decathlon-united', 'facebook',  'instagram',  'livechatinc', 'mailchi', 'pinterest', 'reddit', 'reddress', 'shopperapproved', 'snapchat', 'spigen', 'stevemadden', 'tiktok', 'twitter', 'vimeo', 'wsj', 'youtube']
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

def executeSql(sql,data):
    connection=pymysql.connect(
                                        host="35.224.151.74", #ip
                                        user="root",# usr name
                                        password="", #pwd
                                        db="DomainDB", # db name
                                        charset='utf8'
                                        )
    cs=connection.cursor()
    print(sql)
    cs.executemany(sql,data)
    connection.commit()
    print("The query affected {} rows".format(cs.rowcount))
    cs.close()
    connection.close()


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
        pat = re.compile(r'<title>([\s\S]+)</title>')
        s = re.search(pat,rawtext)
        if s != None:
            temp=str(s.group(1).strip())
            if len(temp)>=255:
                title=temp.split('\n')[0].strip()
                self.ShopIndexPageTitle=title
            else:
                self.ShopIndexPageTitle=temp

        page = pq(rawtext,parser="html")
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
        if productUrl!='':
            rawtext = self.getWebPage(productUrl)
            data=self.parsexml(rawtext)
            if 'urlset' in data.keys() and 'url' in data['urlset'].keys():
                self.ShopNumofProducts=len(data['urlset']['url'])-1 #remove the first domain
            else:
                self.ShopNumofProducts=len(self.reparse(rawtext))-1

   

    def getProductUrl(self):
        rawtext = self.getWebPage(r'https://'+self.url+r'/sitemap.xml')
        lst=self.reparse(rawtext)
        if len(lst)!=0:
            for i in lst:
                if 'product' in i and 'https:' in i and 'cdn' not in i:
                    return i 
        return ''

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
            page = requests.get(links,headers=headers).text
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



sql='''INSERT IGNORE INTO `ShopInfoList`(`ID`,`URL`,`ShopIndexPageTitle`,
    `ShopNumofProducts`,`ShopMonthlyTraffic`,`ShopSocail`,`ShopAveragePriceUSD`,
    `ShopType`,`ShopCountry`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'''

class addRecord():
    def __init__(self):
        self.data=readDomainList()
        self.res=[]
    
    def run(self):
        for i in range(100):
            try:
                temp=self.getRecord(self.data[i][0],self.data[i][1])
                self.res.append(temp)
                print(temp)
            except:
                print('errrr')
        self.writetotxt()
    
    def getRecord(self,id,url):
        shopinf = ShopInfoRecord(id,url)
        data=shopinf.run()
        return data 
    
    def writetotxt(self):
        with open('record.txt','w',encoding='utf-8') as f :
            for i in self.res:
                f.write(str(i))
                f.write('\n')

        
    
    




if __name__ == "__main__":
    #s=addRecord()
    #s.run()
    lst=open('record.txt','r',encoding='utf-8').read().split('\n')[:-1]
    data=[]
    for i in lst:
        data.append(eval(i))
    executeSql(sql,data=data)
    
    
    

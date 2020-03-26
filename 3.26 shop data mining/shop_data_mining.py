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



class SHOP():
    def __init__(self,domain):
        self.domain=domain #域名
        self.url= r'https://'+domain #带https的域名
        self.valid=True #默认可以访问
        self.socialurls=[] # 社交账号
        self.sitemap=[] #sitemap中所有链接
        self.products_num_in_xml=0 #xml中产品数量
        self.products_num_in_json=0 #json中产品数量
        self.products_xml_file_name=domain+'.xml.txt'#xml文件名
        self.products_json_file_name=domain+'.json.txt' #json文件名
        self.get_json_flag=False # 获取json中是否出错
        
        #setting
        self.ua=UserAgent(verify_ssl=False)
        self.headers={"User-Agent": self.ua.chrome}
    
    # func
    def test_and_get_socialurls(self):
        content=''
        try:
            page = requests.get(self.url,headers=self.headers)
        except:
            self.valid=False
            self.products_xml_file_name=''
            self.products_json_file_name=''
            self.get_json_flag='-'
        else:
            if page.status_code!=200:
                self.valid=False
                self.products_xml_file_name=''
                self.products_json_file_name=''
                self.get_json_flag='-'
            else:
                content=page.content
        if content!='':
            page=pq(content,parser="html")
            lst=page('a').items()
            for i in lst:
                temp=i.attr('href')
                if temp!=None and self.domain not in temp and '://' in temp : # 极大化提取所有外链网站
                   self.socialurls.append(temp)
    
    def get_sitemap(self):
        if self.valid==True:
            try:
                page = requests.get(self.url+r'/sitemap.xml',headers=self.headers)
                sitemap=page.text
            except:
                pass 
            else:
                site=pq(sitemap.encode('utf-8'),parser="html")
                self.sitemap=site.text().split('\n') #获取所有的xml 
    

    def get_products_num_in_xml(self):
        if len(self.sitemap)!=0:
            product_url=''
            for i in self.sitemap:
                if 'product' in i:
                    product_url=i
                    break
            if product_url!='':
                res=[]
                try:
                    webdata = requests.get(product_url,timeout=5).text
                    data=pq(webdata.encode('utf-8'),parser='html')
                except:
                    pass
                else:
                    url=data('loc').items()
                    for i in url:
                        temp=self.reparse(str(i))
                        if temp!=''and 'cdn'not in temp:
                            res.append(temp)
                self.products_num_in_xml=len(res)-1
                self.writetotxt(self.products_xml_file_name,res)
                            
    def get_products_num_in_json(self):
        if self.valid==True:
            url = self.url+ '/products.json'
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
                    self.get_json_flag=True
                    error_time-=1
                else:
                    if 'id' not in str(webdata):
                        break
                    temp.append(webdata)
                page+=1
                print(page)
                time.sleep(random.randint(1,3))
            self.writetotxt(self.products_json_file_name,temp)

    #Tools 
    def writetotxt(self,filename,data):
        if type(data)==list and len(data)!=0:
            f=open(r'./urldata/'+filename,'w',encoding='utf-8')
            for i in data:
                f.write(i)
                f.write('\n')
            f.close()
    
    def readfile(self,filename):
        f=open(filename,'r',encoding='utf-8')
        content=f.read().split('\n')
        return content
    
    def count_json_products_num(self):
        filename=r'./urldata/'+ self.products_json_file_name
        content=self.readfile(filename)
        if content!=[]:
            title=[]
            for i in range(len(content)-1):
                jsondata=json.loads(content[i])['products']
                for item in jsondata:
                    title.append(item['title'])
            self.products_num_in_json=len(title)

    def reparse(self,string):
        pat=re.compile(r'\>(.*?)\<')
        s=re.findall(pat,string)
        if len(s)>0:
            return s[0]
        else:
            return None


    #  run
    def run(self):
        self.test_and_get_socialurls()
        if self.valid==True:
            self.get_sitemap()
            self.get_products_num_in_xml()
            self.get_products_num_in_json()
            self.count_json_products_num()
        res=[]
        res.append(self.domain)
        res.append(self.valid)
        res.append(self.socialurls)
        res.append(self.products_num_in_xml)
        res.append(self.products_num_in_json)
        res.append(self.products_xml_file_name)
        res.append(self.products_json_file_name)
        return res 

    
if __name__ == "__main__":
    shop=SHOP('www.nativeunion.com/')
    print(shop.run())



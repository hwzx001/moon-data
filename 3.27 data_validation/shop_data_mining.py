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
import os

# 只进行数据抓取 数据处理全部在data_validation.py中


class SHOP():
    def __init__(self,domain):
        # shop attributes
        self.domain=domain #域名
        self.valid=True #默认可以访问
        self.products_num_in_xml=0 #xml中产品数量
        self.get_json_flag=False # 获取json中是否出错
        self.index_data=''

        self.url= r'https://'+domain #带https的域名
        self.products_xml_file_name=domain+'.xml.txt'#xml文件名
        self.products_json_file_name=domain+'.json.txt' #json文件名

        # setting
        self.ua=UserAgent(verify_ssl=False)
        self.headers={"User-Agent": self.ua.chrome}

        # flush data
        self.url_in_xml=[]
        self.json_data=[]
        self.sitemap=[]
            


    # func
    def get_index_page(self): # 获取首页的内容 同时验证网站是否可以访问
        try:
            page = requests.get(self.url,headers=self.headers)
        except:
            self.valid=False
        else:
            if page.status_code==200:
                self.index_data=page.content
    
    
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
    

    def get_xml_data(self):
        if len(self.sitemap)!=0:
            product_url=''
            for i in self.sitemap:
                if 'product' in i:
                    product_url=i
                    break
            if product_url!='':
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
                            self.url_in_xml.append(temp)
                self.products_num_in_xml=len(self.url_in_xml)-1


                            
    def get_json_data(self):
        if self.valid==True:
            url = self.url+ '/products.json'
            page=1
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
                    self.json_data.append(webdata)
                page+=1
                print(page)
                time.sleep(random.randint(1,3))
            

    #Tools 
    def writetotxt(self,filename,data):
        if type(data)==list and len(data)!=0:
            f=open(filename,'w',encoding='utf-8')
            for i in data:
                f.write(i)
                f.write('\n')
            f.close()

    def reparse(self,string):
        pat=re.compile(r'\>(.*?)\<')
        s=re.findall(pat,string)
        if len(s)>0:
            return s[0]
        else:
            return None

    def write_shop_attr(self):
        with open('attr.txt','w',encoding='utf-8') as f :
            f.write(self.domain)
            f.write('\n')
            f.write(str(self.valid))
            f.write('\n')
            f.write(str(self.products_num_in_xml))
            f.write('\n')
            f.write(str(self.get_json_flag))
        with open('index.txt','w',encoding='utf-8') as f: 
            f.write(str(self.index_data))
    


    #  run
    def run(self):
        self.get_index_page()
        if self.valid==True:
            self.get_sitemap()
            self.get_xml_data()
            self.get_json_data()
        os.mkdir(self.domain)
        os.chdir(self.domain)
        self.write_shop_attr()
        self.writetotxt(self.products_xml_file_name,self.url_in_xml)
        self.writetotxt(self.products_json_file_name,self.json_data)
        self.writetotxt('index.txt',self.index_data)
        self.writetotxt('sitemap.txt',self.sitemap)
        os.chdir('..')
        
       

    
if __name__ == "__main__":
    shop=SHOP('alphaclothing.net')
    shop.run()



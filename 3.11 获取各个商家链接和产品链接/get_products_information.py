import requests
from fake_useragent import UserAgent
import pandas as pd
from pyquery import PyQuery as pq
import time
import random
import re 


def get_page(url):
    try:
        ua = UserAgent(verify_ssl=False)
        headers = {"User-Agent": ua.chrome}
        page = requests.get(url,headers=headers)
        if page.status_code!=200:
            return None
        return page.content
    except:
        return None

def read_file(filename):
    f=open(filename,'r',encoding='utf-8')
    urls=f.read().split('\n')
    return urls

def get_vec(source_code):
    string =str(source_code,encoding='utf-8')
    pat=re.compile(r'window\.ShopifyAnalytics\.lib\.track\([\s]*\"Viewed Product\"\,[\s\S]*\{(.*)\}')
    p=re.search(pat,string)
    if p!=None:
        res=p.groups()
        return res
    else:
        return []



class parse_source_code():
    def __init__(self,source_code):
        self.str=str(source_code,encoding='utf-8')
        self.res=[]
    
    def get_price(self):
        pat=re.compile(r'\"price\":\"([\.0-9]+)\"')
        price=re.findall(pat,self.str)
        if len(price)!=0:
            self.res.append(price)  
        else:
            self.res.append(['-1'])

    def get_created_at(self):
        pat=re.compile(r'\"created_at\":\"(.+)\"')
        created_at=re.findall(pat,self.str)
        if len(created_at)!=0:
            self.res.append(created_at) 
        else:
            self.res.append(['-1'])
    
    def get_name(self):
        pat=re.compile(r'\"name\":\"(.+)\"')
        name=re.findall(pat,self.str)
        if len(name)!=0:
            self.res.append(name) 
        else:
            self.res.append(['-1'])
    
    def parse_data(self):
        #self.get_name()
        self.get_price()
        #self.get_created_at()
        return self.res


        


if __name__ == "__main__":

    urls=read_file('testfile.csv')
    for i in range(len(urls)):
        sourcecode=get_page(urls[i])
        if sourcecode!=None:
            parse=parse_source_code(sourcecode)
            print(parse.parse_data())

    
    


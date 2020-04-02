import requests
from fake_useragent import UserAgent
from pyquery import PyQuery as pq
from multiprocessing.dummy import Pool
import re 
import pandas as pd
import os


class SITEMAP():

    def __init__(self,urls):
        # data
        self.urls=urls

        # setting 
        self.ua=UserAgent(verify_ssl=False)
        self.headers={"User-Agent": self.ua.chrome}

        #multiprocess
        self.threads = 512
        self.count=0



    
    def get_data(self,url):
        flag='TRUE'
        try:
            newurl=r'https://'+str(url)+r'/sitemap.xml'
            sitemap=requests.get(newurl,headers=self.headers,timeout=10).text
        except:
            flag='FASLE'
            self.savetotxt(url,flag,'')
        else:
            self.savetotxt(url,flag,str(sitemap))
        print(self.count)
        self.count+=1


    def multiply_process(self):
        pool = Pool(self.threads)
        pool.map(self.processForMul,range(self.threads))
        pool.close()
        pool.join()

    def process(self,url):
        try:
            self.get_data(url=url)
        except:
            self.savetotxt(url,'FASLE','')

    def savetotxt(self,url,flag,data):
        with open(url+'.txt','w',encoding='utf-8') as f:
            f.write(flag)
            f.write('\n')
            if data!='':
                f.write(data)
                f.write('\n')

    def processForMul(self,threads):
        for i in range(threads,len(self.urls),self.threads):
            self.process(self.urls[i])

if __name__ == "__main__":
    lst=open('data.txt').read().split('\n')[1:1000]
    os.mkdir('sitemaptxt')
    os.chdir('sitemaptxt')
    a=SITEMAP(lst)
    a.multiply_process()
    
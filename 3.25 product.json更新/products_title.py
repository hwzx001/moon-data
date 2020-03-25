import requests
import json
import pandas as pd
from multiprocessing.dummy import Pool
import os
import time
import random

class mult_process():
    def __init__(self,domains):
        self.domains=domains
        self.error=[] #保存错误结果
        self.threads = 32
        self.count=0

    def get_json_data(self,domain): # 获取单个网站的product.json
        url = str('https://')+str(domain)+ '/products.json'
        try:
            webdata = requests.get(url,timeout=5).text
        except:
            self.error.append(domain)
        else:
            self.savetotxt(domain=domain,data=webdata)
        print(self.count)
        self.count+=1

    def savetotxt(self,domain,data):
        f=open('jsonres/'+domain+'.json.txt','w',encoding='utf-8')
        f.write(data)
        f.close()


    def multiply_process(self):
        pool = Pool(self.threads)
        pool.map(self.processForMul,range(self.threads))
        pool.close()
        pool.join()

    def process(self,domain):
        try:
            self.get_json_data(domain)
        except:
            print(domain +' : ERROR')

    def processForMul(self,threads):
        for i in range(threads,len(self.domains),self.threads):
            self.process(self.domains[i])

    def handleError(self):
        f=open('wrong.txt','w',encoding='utf-8')
        for i in self.error:
            f.write(i)
            f.write('\n')
        f.close()


if __name__ == "__main__":
    lst=['www.nativeunion.com','www.colourpop.com']
    s=mult_process(lst)
    s.multiply_process()
    s.handleError()


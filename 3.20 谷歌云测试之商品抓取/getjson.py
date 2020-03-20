import requests
import json
import pandas as pd
from multiprocessing.dummy import Pool
import os
import time
import random
def save_to_csv(shop_list,filename):
    data = pd.DataFrame(shop_list)
    data.to_csv(filename+'.csv', mode='a', index=False, sep=',', header=False,encoding='utf-8')


class mult_process():
    def __init__(self,domain_name):
        self.domain_name=domain_name # 带txt的域名
        self.names=[] # 所有的商品名
        self.res=[] #保存结果
        self.threads = 4
        self.domain=str(domain_name).replace('.txt','') #不带txt的域名

    def get_names(self):
        f = open(self.domain_name, 'r', encoding='utf-8')
        self.names = f.read().split('\n')[:-1]

    def get_json_data(self,productname): # 获取单个商品的json
        temp=[]
        temp.append(productname)
        url = r'https://' + str(self.domain) + '/products/' + str(productname) + '.js'
        try:
            webdata = requests.get(url).text
            data = json.loads(webdata)
        except:
            temp.append('')
            self.res.append(temp)
        else:
            temp.append(str(data))
            self.res.append(temp)
        time.sleep(random.randint(1, 5))

    def multiply_process(self):
        pool = Pool(self.threads)
        pool.map(self.processForMul,range(self.threads))
        pool.close()
        pool.join()

    def process(self,productname):
        try:
            self.get_json_data(productname)
        except:
            print(productname+'error')

    def processForMul(self,threads):
        for i in range(threads,len(self.names),self.threads):
            self.process(self.names[i])

    def save_to_csv(self):
        data = pd.DataFrame(self.res)
        data.to_csv(self.domain + '.csv', mode='a', index=False, sep=',', header=False, encoding='utf-8')

    def run(self):
        self.get_names()
        self.multiply_process()
        os.chdir('../data')
        self.save_to_csv()


if __name__ == "__main__":
    #0-6.no
    os.chdir(r'D:\a\newdata')
    mul=mult_process('0-6.no.txt')
    mul.run()

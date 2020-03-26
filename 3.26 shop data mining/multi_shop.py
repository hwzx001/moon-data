import requests
import json
import pandas as pd
from multiprocessing.dummy import Pool
from shop_data_mining import SHOP
class mult_process():
    def __init__(self,domains):
        self.domains=domains
        self.threads = 32
        self.count=0
        self.res=[]

    def savetoscv(self):
        data = pd.DataFrame(self.res)
        names=['Domain','Valid','socialUrls','xmlNums','JsonNums','xmlFilename','jsonFilename']
        data.to_csv('Shop_List.csv', mode='a', index=True, sep=',', header=names,encoding='utf-8')

    def process_shop(self,domain):
        shop=SHOP(domain)
        data=shop.run()
        self.res.append(data)

    def multiply_process(self):
        pool = Pool(self.threads)
        pool.map(self.processForMul,range(self.threads))
        pool.close()
        pool.join()

    def process(self,domain):
        try:
            self.process_shop(domain)
        except:
            print(domain +' : ERROR')

    def processForMul(self,threads):
        for i in range(threads,len(self.domains),self.threads):
            self.process(self.domains[i])




if __name__ == "__main__":
    lst=open('data.txt','r',encoding='utf-8').read().split('\n')[100:120]
    s=mult_process(lst)
    s.multiply_process()
    s.savetoscv()


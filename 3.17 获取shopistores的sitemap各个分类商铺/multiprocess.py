from multiprocessing import Pool
from crawl_classification import down_classification
import os
class mult_process():
    def __init__(self,shop_urls):
        self.shop_urls=shop_urls
        self.threads = 16
        self.count=0
        #self.res=[]

    def multiply_process(self):
        pool = Pool(self.threads)
        pool.map(self.processForMul, range(self.threads))
        pool.close()
        pool.join()

    def process(self, url):
        spi = down_classification(url)
        spi.down()
        try:
            spi = down_classification(url)
            spi.down()
        except:
            print(url + ' error')

    def processForMul(self, threads):
        for i in range(threads, len(self.shop_urls), self.threads):
            self.process(self.shop_urls[i])
            print(self.count)
            self.count+=1

if __name__ == '__main__':
    lst = open('siemapresult.txt', 'r', encoding='utf-8').read().split('\n')
    os.chdir(r'D:\a\tempdata\3.17')
    mult=mult_process(shop_urls=lst)
    mult.multiply_process()
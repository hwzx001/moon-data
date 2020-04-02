import requests
from fake_useragent import UserAgent
from pyquery import PyQuery as pq
from multiprocessing.dummy import Pool
import re 
import pandas as pd

class SITEMAP():

    def __init__(self,urls):
        # data
        self.urls=urls
        self.res=[]

        # setting 
        self.ua=UserAgent(verify_ssl=False)
        self.headers={"User-Agent": self.ua.chrome}

        #multiprocess
        self.threads = 256
        self.count=0



    
    def get_data(self,url):
        record=[] # 数据：url、IsValid、sitemap 
        record.append(url)
        record.append('TRUE')
        try:
            newurl=r'https://'+str(url)+r'/sitemap.xml'
            sitemap=requests.get(newurl,headers=self.headers,timeout=10).text
        except:
            record[1]='FASLE'
            record.append([])
        else:
            record.append(self.reparse(str(sitemap)))
            ''' # 用pyquery处理会出问题 
            site=pq(sitemap.encode('utf-8'),parser="html")
            sitemap=site.text().split('\n') #获取所有的xml 
            record.append(sitemap)
            '''
        self.res.append(record)
        print(self.count)
        self.count+=1

    # use the regression to parse the string 
    def reparse(self,string):
        pat=re.compile(r'\>(.*?)\<')
        s=re.findall(pat,string)
        return s 

    def multiply_process(self):
        pool = Pool(self.threads)
        pool.map(self.processForMul,range(self.threads))
        pool.close()
        pool.join()

    def process(self,url):
        try:
            self.get_data(url=url)
        except:
            self.res.append([url,'FASLE',[]])

    def processForMul(self,threads):
        for i in range(threads,len(self.urls),self.threads):
            self.process(self.urls[i])

    def savetocsv(self):
        data = pd.DataFrame(self.res)
        names = ['URL', 'IsValid', 'SiteMap']
        data.to_csv('SitemapRes.csv', mode='a', index=False, sep=',', header=names, encoding='utf-8')

if __name__ == "__main__":
    lst=open('data.txt').read().split('\n')[0:2000]
    a=SITEMAP(lst)
    a.multiply_process()
    a.savetocsv()
    
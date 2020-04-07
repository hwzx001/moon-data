from multiprocessing.dummy import Pool
import re 
import requests 
import os
import pymysql 
import pymysql.cursors
from fake_useragent import UserAgent

class DomainTest():
    def __init__(self,urls):
        # data
        self.urls=urls
        #multiprocess
        self.threads = 2048
        self.count=0
        self.usrvalue=[]

        self.ua=UserAgent(verify_ssl=False)
        self.headers={"User-Agent": self.ua.chrome}


    def get_data(self,url):
        self.count+=1
        print(self.count)
        try:
            newurl=r'https://'+str(url)
            page = requests.get(newurl,headers=self.headers,timeout=10)
            data=page.text
        except:
            return (url,'0')
        else:
            if data!='':
                return (url,'1')
            else:
                return (url,'0')

    def multiply_process(self):
        pool = Pool(self.threads)
        pool.map(self.processForMul,range(self.threads))
        pool.close()
        pool.join()

    def process(self,url):
        try:
            res=self.get_data(url=url)
        except:
            res=(url,'0')
        self.usrvalue.append(res)
            

    def processForMul(self,threads):
        for i in range(threads,len(self.urls),self.threads):
            self.process(self.urls[i])

    def writetodb(self):
        connection=pymysql.connect(
                                        host="35.224.151.74", #ip
                                        user="root",# usr name
                                        password="******", #pwd
                                        db="DomainDB", # db name
                                        charset='utf8'
                                        )
        cs=connection.cursor()
        cs.executemany('INSERT IGNORE INTO `DomainList`(`URL`,`IsValid`) VALUES (%s,%s)',self.usrvalue)
        connection.commit()
        print("The query affected {} rows".format(cs.rowcount))
        cs.close()
        connection.close()
        print('okkkkk')
    
    def run(self):
        self.multiply_process()
        self.writetodb()

if __name__ == "__main__":
    lst=open("data.txt",'r',encoding='utf-8').read().split('\n')
    dom=DomainTest(lst)
    dom.run()
   

    

'''
Name    : Domain Name Validation
Version : 0.1.1
Updates Time: 2020.04.10
Author  : Lucky 
Update Content ：
    1、modify：class DomainTest
        --added concurrent processing of processes

    2、modify：fun   get_data
        --first write the content to a file, then write to the database(InsertDomain.py)
        
    3、delete: fun   writetodb

'''


from multiprocessing.dummy import Pool,Lock
import re 
import requests 
import os
import pymysql 
import pymysql.cursors
from fake_useragent import UserAgent
from datetime import datetime

lock=Lock()
Date=datetime.now().strftime('%Y-%m-%d')
class DomainTest():
    def __init__(self,urls):
        # data
        self.urls=urls
        #multiprocess
        self.threads =1024
        self.count=0
        self.f=open('DomainList'+str(Date)+'.txt','w',encoding='utf-8')

        self.ua=UserAgent(verify_ssl=False)
        self.headers={"User-Agent": self.ua.chrome}
    
    def __del__(self):
         self.f.close()


    def get_data(self,url):
        record=[url,'1']
        try:
            newurl=r'https://'+str(url)
            page = requests.get(newurl,headers=self.headers,timeout=10)
            data=page.text
        except:
            record[1]='0'
        else:
            if data=='':
                record[1]='0'
        finally:
            return tuple(record)
              

    def multiply_process(self):
        pool = Pool(self.threads)
        pool.map(self.processForMul,range(self.threads))
        pool.close()
        pool.join()

    def process(self,url):
        self.count+=1
        print(self.count)
        try:
            res=self.get_data(url=url)
        except:
            res=(url,'0')
        finally:
            lock.acquire()
            self.f.write(str(res))
            self.f.write('\n')
            lock.release()

    def processForMul(self,threads):
        for i in range(threads,len(self.urls),self.threads):
            self.process(self.urls[i])
    
    '''
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
    '''

    def run(self):
        self.multiply_process()

if __name__ == "__main__":
    lst=open("data.txt",'r',encoding='utf-8').read().split('\n')[0:2000]
    dom=DomainTest(lst)
    dom.run()
   

    

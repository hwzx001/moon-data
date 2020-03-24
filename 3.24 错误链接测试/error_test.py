import requests
from multiprocessing.dummy import Pool
# To do: learn APScheduler


class exceptionsDiffer():
    def __init__(self,urls):
        self.urls=urls
        self.connectionerror=[]
        self.Error404=[]
        self.HTTPError=[]
        self.unKnowError=[]
        self.ConnectTimeout=[]
        self.threads = 24
        self.count=0
    
    def writetotxt(self,arr,name):
        f=open(name+'.txt','w',encoding='utf-8')
        for i in arr:
            f.write(i)
            f.write('\n')
        f.close

    def differ(self,url):
        try:
            s=requests.get(r'http://'+url+r'/procudts.js',timeout=5) # 判断products.js是否可以访问 超时时长设置为5s
        except requests.exceptions.ConnectionError: #连接异常
            self.connectionerror.append(url)
        except requests.exceptions.HTTPError: # http 异常
            self.HTTPError.append(url)
        except requests.exceptions.ConnectTimeout: #超时
            self.ConnectTimeout.append(url)
        except:
            self.unKnowError.append(url) #未知
        else:
            if s.status_code==404: #404 异常
                self.Error404.append(url)
            else: #其他情况
                self.unKnowError.append(url)
        print(self.count)
        self.count+=1
    
    def out(self):
        self.writetotxt(self.unKnowError,'unKnowError')
        self.writetotxt(self.connectionerror,'connectionerror')
        self.writetotxt(self.Error404,'Error404')
        self.writetotxt(self.HTTPError,'HTTPError')
        self.writetotxt(self.ConnectTimeout,'ConnectTimeout')
    

    def multiply_process(self):
        pool = Pool(self.threads)
        pool.map(self.processForMul,range(self.threads))
        pool.close()
        pool.join()

    def process(self,url):
        try:
            self.differ(url)
        except:
            print(url +' : ERROR')

    def processForMul(self,threads):
        for i in range(threads,len(self.urls),self.threads):
            self.process(self.urls[i])
    
    def run(self):
        self.multiply_process()
        self.out()
            


if __name__ == "__main__":
    lst=open('domains.txt','r',encoding='utf-8').read().split('\n')
    ex=exceptionsDiffer(lst)
    ex.run()

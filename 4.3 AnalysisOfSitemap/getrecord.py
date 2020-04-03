from multiprocessing.dummy import Pool
import re 
import os
import pandas as pd 

os.chdir('sitemaptxt')
class AnalysisOfSite():

    def __init__(self,filenames):
        # data
        self.filenames=filenames
        #multiprocess
        self.threads = 2048
        self.count=0
        self.res=[]
    


    def get_data(self,filename):
        with open(filename) as f:
            flag = f.readline().strip()
            if flag==False:
                return 0,None,None
            else:
                product=''
                lst=self.reparse(str(f.read()))
                otherURL=[]
                for i in lst:
                    if i!='':
                        if 'products' in i:
                            product=i
                        elif 'https' in i:
                            otherURL.append(i)
                return 1,product,str(otherURL)
    
    def product_record(self,filename):
        url=str(filename)[:-4]
        flag,product,otherURL=self.get_data(filename)
        self.res.append([url,flag,product,otherURL])
        print(self.count)
        self.count+=1
        

    def reparse(self,string):
        pat=re.compile(r'\>(.*?)\<')
        s=re.findall(pat,string)
        return s 

    def multiply_process(self):
        pool = Pool(self.threads)
        pool.map(self.processForMul,range(self.threads))
        pool.close()
        pool.join()

    def process(self,filename):
        try:
            self.product_record(filename=filename)
        except:
            pass 

    def processForMul(self,threads):
        for i in range(threads,len(self.filenames),self.threads):
            self.process(self.filenames[i])

    def writetocsv(self):
        data = pd.DataFrame(self.res)
        names = ['URL', 'IsValid', 'ProductURL','OtherURL']
        data.to_csv('SitemapRes.csv', mode='a', index=False, sep=',', header=names, encoding='utf-8')
        

if __name__ == "__main__":
    lst=os.listdir()
    a=AnalysisOfSite(lst)
    a.multiply_process()
    os.chdir('..')
    a.writetocsv()
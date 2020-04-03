from multiprocessing.dummy import Pool
import re 
import os
import pymysql 
import pymysql.cursors

os.chdir('sitemaptxt')
class AnalysisOfSite():

    def __init__(self,filenames):
        # data
        self.filenames=filenames
        #multiprocess
        self.threads = 2048
        self.count=0
        self.usrvalue=[]

    ''' Unknown Error  pymysql.err.InterfaceError: (0, '')
    def __del__(self):
        self.connection.close()
    '''
    


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
        self.usrvalue.append((url,flag,product,otherURL))
        print(self.count)
        self.count+=1
        if self.count%200000==0: #每20000条写一次
            self.writetodb(self.usrvalue)
            self.usrvalue=[]

      

        '''
        with self.connection.cursor() as cursor:
            sql = "INSERT INTO `MASTERLIST_test`(`URL`,`Isvalid`,`ProductURL`,`OtherURL`) VALUES (%s,%s,%s,%s);"
            cursor.execute(sql, (url,flag,product,otherURL,))'''

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

    def writetodb(self,data):
        connection=pymysql.connect(
                                        host="35.224.151.74", #ip
                                        user="root",# usr name
                                        password="971231", #pwd
                                        db="SiteMap", # db name
                                        charset='utf8'
                                        )
        cs=connection.cursor()
        cs.executemany('INSERT IGNORE INTO `MASTERLIST`(`URL`,`Isvalid`,`ProductURL`,`OtherURL`) VALUES (%s,%s,%s,%s)',data)
        connection.commit()
        cs.close()
        connection.close()
        print('okkkkk')

if __name__ == "__main__":
    lst=os.listdir()
    a=AnalysisOfSite(lst)
    a.multiply_process()
    
from getjson import mult_process
from multiprocessing.dummy import Pool
import os
import time
import random

class mult_shop():
    def __init__(self,names):
        self.names=names
        self.threads = 8
    def multiply_process(self):
        pool = Pool(self.threads)
        pool.map(self.processForMul,range(self.threads))
        pool.close()
        pool.join()
    def process(self,name):
        try:
            s=mult_process(domain_name=name)
            s.run()
            time.sleep(random.randint(1,5))
        except:
           pass
    def processForMul(self,threads):
        for i in range(threads,len(self.names),self.threads):
            self.process(self.names[i])
if __name__ == '__main__':
    namelst=os.listdir('./inputtxt')
    os.chdir('inputtxt')
    s=mult_shop(namelst)
    s.multiply_process()
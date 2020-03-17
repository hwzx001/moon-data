import os
import pandas as pd

urls=os.listdir('D:/a/data')
os.chdir('D:/a/data')

res=[]

f=open('result.txt','w',encoding='utf-8')
names = ['urls']
for i in range(len(urls)):
    data = pd.read_csv(urls[i], header=None, names=names,encoding='utf-8')
    temp=data['urls']
    if len(temp)>1 and str(temp[1])[0]=='h':
        #print(temp[1])
        f.write(str(temp[1]))
        f.write('\n')
f.close()
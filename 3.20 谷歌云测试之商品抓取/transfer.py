import os
import pandas as pd
os.chdir(r'D:\a\newdata')

def readfile(filename):
    file=r'D:\\a\\data\\'+filename
    names=['url']
    data = pd.read_csv(file, header=0, names=names, encoding='utf-8')
    res=[]
    for item in data['url']:
        temp=str(item).split('/')
        if len(temp)!=0 :
            if temp[-1]!='':
                res.append(temp[-1])
    return res
def savetotext(url,res):
    f=open(url+'.txt','w',encoding='utf-8')
    for i in res:
        f.write(i)
        f.write('\n')
    f.close()


if __name__ == '__main__':
    lst=os.listdir(r'D:\a\data')
    for i in range(len(lst)):
        url=lst[i].replace('.csv','')
        temp=readfile(lst[i])
        savetotext(url,temp)
import json 
import os
os.chdir('jsonres')

def readfile(filename):
    f=open(filename,'r',encoding='utf-8')
    content=f.read()
    jsondata=json.loads(content)['products']
    title=[]
    for i in jsondata:
        title.append(i['title'])
    return title

if __name__ == "__main__":
    print(readfile('www.nativeunion.com.json.txt'))
    
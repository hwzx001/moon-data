import json 
import os
import requests
from pyquery import PyQuery as pq
import re
os.chdir('jsonres')

def readfile(filename):
    f=open(filename,'r',encoding='utf-8')
    content=f.read().split('\n')
    title=[]
    for i in range(len(content)-1):
        jsondata=json.loads(content[i])['products']
        for item in jsondata:
            title.append(item['title'])
    return title



#<title>Night Cable</title>
def reparse(string):
    pat=re.compile(r'\>(.*?)\<')
    s=re.findall(pat,string)
    if len(s)>0:
        return s[0]
    else:
        return None


def getxml(url):
    webdata = requests.get(url,timeout=5).text
    data=pq(webdata.encode('utf-8'),parser='html')
    res=data('title').items()
    title=[]
    for i in res:
        temp=reparse(str(i))
        if temp!=None:
            title.append(temp)
    return title
    




if __name__ == "__main__":
    xml_title=getxml('https://colourpop.com/sitemap_products_1.xml?from=7141886663&to=4548076044370')
    products_title=readfile('www.colourpop.com.json.txt')
    print(len(xml_title))
    print(len(products_title))
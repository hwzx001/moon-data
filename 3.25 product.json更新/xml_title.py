import requests
from pyquery import PyQuery as pq
import re

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
    url='https://www.nativeunion.com/sitemap_products_1.xml?from=1583099838582&to=4499226493067'
    print(getxml(url=url))
    
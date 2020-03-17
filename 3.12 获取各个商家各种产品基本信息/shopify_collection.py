import requests
from fake_useragent import UserAgent
import pandas as pd
from pyquery import PyQuery as pq
from multiprocessing.dummy import Pool
import time
import random

error=[]
def get_page(url):
    try:
        ua = UserAgent(verify_ssl=False)
        headers = {"User-Agent": ua.chrome}
        page = requests.get(url,headers=headers)
        if page.status_code!=200:
            error.append(url)
            return None
        return page.text
    except:
        error.append(url)
        return None
def save_to_csv(item,filename):
    data = pd.DataFrame(item)
    data.to_csv(r'D:/a/data/'+filename+'.csv', mode='a', index=False, sep=',', header=False,encoding='utf-8')
def get_sitemap_products_url(shop_url):
    url='https://'+shop_url+'/sitemap.xml' #必须要加https
    try:
        sitemap=get_page(url=url)
        if sitemap==None:
            return ''
    except:
        return ''
    else:
        site=pq(sitemap.encode('utf-8'),parser="html")
        urls=site.text().split('\n') #获取所有的xml 但是只有带products的才是商品页
        #print(urls)
        for i in urls:
            if 'products'in i:
                return i
        return ''
def get_product_information(sitemap_products_url):
    try:
        xml=get_page(sitemap_products_url)
    except:
        print('ERROR')
        return 0
    else:
        if xml!=None:
            data = pq(xml.encode('utf-8'), parser="html")
            infor = data.text().split('\n')
            return infor
        else:
            #print(r'Can Not Got Information! ')
            return ''
def parse_infor(infor,filename):
    res = []
    #temp=[]
    #print(infor)
    for i in range(len(infor)):
        if 'https' in infor[i] and 'jpg'not in infor[i] and 'cdn' not in infor[i] and infor[i][0]=='h':
            res.append([infor[i]])
    if res!=[]:
        save_to_csv(res,filename)
    else:
        print( filename+'  wrong!')

def down_shop_urls(shop_urls):
    for i in shop_urls:
        sitemap_products_url = get_sitemap_products_url(shop_url=i)
        infor = get_product_information(sitemap_products_url)
        parse_infor(infor, i)

class mult_process():
    def __init__(self,shop_urls):
        self.shop_urls=shop_urls
        self.threads = 8
    def multiply_process(self):
        pool = Pool(self.threads)
        pool.map(self.processForMul,range(self.threads))
        pool.close()
        pool.join()
    def process(self,url):
        try:
            sitemap_products_url = get_sitemap_products_url(shop_url=url)
            infor = get_product_information(sitemap_products_url)
            parse_infor(infor, url)
        except:
            print(url+'error')
    def processForMul(self,threads):
        for i in range(threads,len(self.shop_urls),self.threads):
            self.process(self.shop_urls[i])


def test():
    url=input('Please enter the store URL:')
    sitemap_products_url = get_sitemap_products_url(shop_url=url)
    infor = get_product_information(sitemap_products_url)
    parse_infor(infor, url)


if __name__ == '__main__':
    names = ['#', 'Store Address', 'Title', 'Alexa', 'Best Selling', 'Country']
    data = pd.read_csv(r'shopistores.csv', header=None, names=names, encoding='utf-8')
    urls=list(data['Store Address'])
    p = mult_process(urls)
    p.multiply_process()
    f=open('error.txt','w',encoding='utf-8')
    for i in error:
        f.write(i)
        f.write('\n')
    f.close()



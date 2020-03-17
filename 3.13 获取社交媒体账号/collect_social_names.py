import requests
from pyquery import PyQuery as pq
from fake_useragent import UserAgent
import pandas as pd
from multiprocessing import Pool

def get_page(url):
    try:
        ua = UserAgent(verify_ssl=False)
        headers = {"User-Agent": ua.chrome}
        page = requests.get(url,headers=headers)
        if page.status_code!=200:
            return None
        return page.content
    except:
        return None

social_keys=['amazon', 'boards', 'businessinsider', 'citiesocial', 'cyrillcase', 'decathlon-united', 'desk', 'facebook', 'fleshjack', 'instagram', 'instyle', 'livechatinc', 'mailchi', 'pinterest', 'reddit', 'reddress', 'shopperapproved', 'snapchat', 'spigen', 'stevemadden', 'tiktok', 'twitter', 'vimeo', 'wsj', 'youtube']
def parse_source(raw_url):
    url=r'https://'+raw_url+r'/'
    content=get_page(url)
    res=[]
    res.append(raw_url)
    if content!=None:
        page=pq(content,parser="html")
        lst=page('a').items()
        for i in lst:
            temp=i.attr('href')
            if temp!=None and raw_url not in temp and '://' in temp : # 极大化提取所有外链网站
                res.append(temp)
            '''
            if temp!=None: # 极小化提取 根据给定的list对比 但是有可能会漏掉一些网站
                for j in social_keys:
                    if j in temp:
                        print(temp)
            '''
    return res
                

def read_shopistorescsv():
    names = ['#', 'Store Address', 'Title', 'Alexa', 'Best Selling', 'Country']
    data = pd.read_csv(r'shopistores.csv', header=None, names=names, encoding='utf-8')
    urls=list(data['Store Address'])
    return urls

class mult_process():
    def __init__(self,shop_urls):
        self.shop_urls=shop_urls
        self.threads = 16
        self.count=0
        #self.res=[]

    def get_page(self,url):
        try:
            ua = UserAgent(verify_ssl=False)
            headers = {"User-Agent": ua.chrome}
            page = requests.get(url, headers=headers)
            if page.status_code != 200:
                return None
            return page.content
        except:
            return None

    def parse_source(self,raw_url):
        url = r'https://' + raw_url + r'/'
        content = self.get_page(url)
        res = []
        res.append(raw_url)
        if content != None:
            page = pq(content, parser="html")
            lst = page('a').items()
            for i in lst:
                temp = i.attr('href')
                if temp != None and raw_url not in temp and '://' in temp:  # 极大化提取所有外链网站
                    res.append(temp)
        self.count+=1
        print(self.count)
        #print(res)
        self.save_to_csv([res])

    def multiply_process(self):
        pool = Pool(self.threads)
        pool.map(self.processForMul,range(self.threads))
        pool.close()
        pool.join()
    def process(self,url):
        try:
            self.parse_source(url)
        except:
            print(url+' error')
    def processForMul(self,threads):
        for i in range(threads,len(self.shop_urls),self.threads):
            self.process(self.shop_urls[i])

    def save_to_csv(self,item):
        data = pd.DataFrame(item)
        data.to_csv(r'SocialInformation' + '.csv', mode='a', index=False, sep=',', header=False, encoding='utf-8')


if __name__ == "__main__":
    #url='colourpop.com'
    #url='jeffreestarcosmetics.com'
    #url='fashionnova.com'
    #print(parse_source(raw_url=url))
    urls=read_shopistorescsv()
    mult=mult_process(shop_urls=urls)
    mult.multiply_process()

import pymysql 
import pymysql.cursors
import requests
from fake_useragent import UserAgent
from pyquery import PyQuery as pq
import re 

class xmllist():

    # create connection 
    def __init__(self,urls):

        self.connection=pymysql.connect(
        host="35.224.151.74", #ip
        user="root",# usr name
        password="******", #pwd
        db="ShopList", # db name
        charset='utf8'
    )
        self.cursor=self.connection.cursor()
        self.urls=urls

        self.ua=UserAgent(verify_ssl=False)
        self.headers={"User-Agent": self.ua.chrome}

    # close the connection 
    def __del__(self):
        self.connection.close()


    #create table shoplist
    def create_table(self,url): 
        sql='''CREATE TABLE `'''+str(url)+'''` (
            `No` int(11) NOT NULL AUTO_INCREMENT,
            `URL` varchar(255) COLLATE utf8_bin NOT NULL,
            PRIMARY KEY (`No`))
             ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin AUTO_INCREMENT=1 ;
        '''
        self.cursor.execute(sql)
        self.connection.commit()
 

    def writetodb(self,url,data):
        self.create_table(url)
        if len(data)>=0:
            for i in data:
                try:
                    # Create a new record
                    sql = "INSERT INTO `"+str(url)+"` (`URL`) VALUES (%s)"
                    self.cursor.execute(sql, (i))
                except:
                    pass
            # commit 
            self.connection.commit()


    def get_data(self,url):
        res=[]
        try:
            newurl=r'https://'+str(url)+r'/sitemap.xml'
            page = requests.get(newurl,headers=self.headers)
            sitemap=page.text
        except:
            pass 
        else:
            site=pq(sitemap.encode('utf-8'),parser="html")
            sitemap=site.text().split('\n') #获取所有的xml 
            if len(sitemap)!=0:
                product_url=''
                for i in sitemap:
                    if 'product' in i:
                        product_url=i
                        break
                if product_url!='':
                    try:
                        webdata = requests.get(product_url,timeout=5).text
                        data=pq(webdata.encode('utf-8'),parser='html')
                    except:
                        pass
                    else:
                        url=data('loc').items()
                        for i in url:
                            temp=self.reparse(str(i))
                            if temp!=''and 'cdn'not in temp:
                                res.append(temp)

        return res

    def reparse(self,string):
        pat=re.compile(r'\>(.*?)\<')
        s=re.findall(pat,string)
        if len(s)>0:
            return s[0]
        else:
            return None

    def run(self):
        for url in self.urls:
            data=self.get_data(url=url) 
            self.writetodb(url=url,data=data)



if __name__ == "__main__":
    #lst=['colourpop.com','www.nativeunion.com']
    lst=open('data.txt').read().split('\n')[10:20]
    s=xmllist(urls=lst)
    s.run()
    

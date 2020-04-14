import pymysql 
import pymysql.cursors
import pandas as pd 
import numpy as np

def writetodb(data):
    connection=pymysql.connect(
                                host="35.224.151.74", #ip
                                user="root",# usr name
                                password="", #pwd
                                db="DomainDB", # db name
                                charset='utf8'
                                )
    cs=connection.cursor()
    cs.executemany('INSERT IGNORE INTO `DomainList_test`(`URL`,`IsValid`) VALUES (%s,%s)',data)
    connection.commit()
    print("The query affected {} rows".format(cs.rowcount))
    cs.close()
    connection.close()
    print('okkkkk')


def parsedomain(domain):
    if domain!='' :
        temp=str(domain).split('.')
        string='.'
        if temp[0]=='www':
            res=string.join(temp[1:])
            return res 
        else:
            return domain

names=['rank', 'URL', 'ShopIndexPageTitle', 'ShopCountry', 'status', 'platform', 'platform rank', 
'plan', 'ShopCreated', 'twitter', 'twitter followers', 'facebook', 'facebook followers', 
'instagram', 'instagram followers', 'pinterest', 'pinterest followers', 'snapchat', 
'email', 'phone', 'youtube', 'youtube followers', 'linkedin', 'theme', 
'theme spend', 'ThemeVendor', 'InstalledApps', 'monthly app spend',
 'aliases', 'products sold', 'vendor count', 'Categories', 'alexa rank',
  'Technologies', 'Currency', 'average price', 'estimated sales']
def read_shopistorescsv():
    data = pd.read_csv(r'D:\a\Shopify Store Leads\allshopify.csv',names=names,encoding='utf-8')
    data=data.fillna(value="NULL")
    with open('ShopBaseInfo.txt','w',encoding='utf-8') as f :
        for i in range(1,len(data)):
            print(i)
            temp=str(parseRecord(data.iloc[i]))
            f.write(temp)
            f.write('\n')

    
def parseRecord(record):
    res=[]
    res.append(parsedomain(record['URL']))
    res.append(1)
    res.append(record['ShopIndexPageTitle'])
    res.append(record['Technologies'])
    res.append(record['ShopCountry'])
    res.append(record['ShopCreated'])
    social={}
    s=['twitter', 'facebook', 'instagram', 'pinterest',  'snapchat', 'email', 'phone', 'youtube', 'linkedin']
    for i in s:
        if record[i]!='' and str(record[i]) != 'NULL':
            social[i]=record[i]
    res.append(str(social))
    res.append(record['ThemeVendor'])
    res.append(record['InstalledApps'])
    res.append(record['Categories'])
    res.append(record['Currency'])
    return tuple(res) 

if __name__ == "__main__":
    read_shopistorescsv()

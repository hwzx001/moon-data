
import pymysql 
import pymysql.cursors

def executeSql(sql,data):
    connection=pymysql.connect(
                                        host="35.224.151.74", #ip
                                        user="root",# usr name
                                        password="", #pwd
                                        db="DomainDB", # db name
                                        charset='utf8'
                                        )
    cs=connection.cursor()
    print(sql)
    cs.executemany(sql,data)
    connection.commit()
    print("The query affected {} rows".format(cs.rowcount))
    cs.close()
    connection.close()

sql='''INSERT IGNORE INTO `ShopInfoList`(`ID`,`URL`,`ShopIndexPageTitle`,
    `ShopNumofProducts`,`ShopMonthlyTraffic`,`ShopSocail`,`ShopAveragePriceUSD`,
    `ShopType`,`ShopCountry`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'''



if __name__ == "__main__":
    lst=open('ShopListRecord2020-04-09.txt','r',encoding='utf-8').read().split('\n')
    temp=[]
    for i in lst:
        if i!='':
            temp.append(eval(i))
    executeSql(sql,temp)
    

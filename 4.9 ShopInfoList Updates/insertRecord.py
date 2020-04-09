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

    lst=open('record.txt','r',encoding='utf-8').read().split('\n')[:-1]
    data=[]
    for i in lst:
        data.append(eval(i))
    executeSql(sql,data=data)

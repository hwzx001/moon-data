'''
Name    : Insert Record Into DomainList
Version : 0.1.2
Updates Time: 2020.04.14
Author  : Lucky 
Update Content ：
        1、Modify 
            --sql
        2、Modify 
            --main
'''




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
    cs.executemany(sql,data)
    connection.commit()
    print("The query affected {} rows".format(cs.rowcount))
    cs.close()
    connection.close()

sql='''INSERT IGNORE INTO `ShopBaseInfo`(`URL`,`IsValid`,`ShopIndexPageTitle`,
    `Technologies`,`ShopCountry`,`ShopCreated`,`ShopSocial`,`ThemeVendor`,
    `InstalledApps`,`Categories`,`Currency`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''



if __name__ == "__main__":
    lst=open('ShopBaseInfo.txt','r',encoding='utf-8').read().split('\n')
    temp=[]
    for i in lst:
        if i!='':
            temp.append(eval(i))
    executeSql(sql,temp)
    

import pandas as pd 
import os
os.chdir(r'D:\a\Shopify Store Leads')
def read_shopistorescsv():
    #names = ['#', 'Store Address', 'Title', 'Alexa', 'Best Selling', 'Country']
    data = pd.read_csv(r'allshopify.csv', header=None,  encoding='utf-8')
    domain=data[1]
    f=open('newdata.txt','w',encoding='utf-8')
    for i in domain:
        temp=str(i).split('.')
        string='.'
        
        if temp[0]=='www':
            res=string.join(temp[1:])
        else:
            res=string.join(temp)
        f.write(res)
        f.write('\n')
    f.close()
    #urls=list(data['Store Address'])
    #return urls


if __name__ == "__main__":
    read_shopistorescsv()
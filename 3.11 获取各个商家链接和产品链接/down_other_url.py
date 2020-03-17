import os
import pandas as pd

names = ['#', 'Store Address', 'Title', 'Alexa', 'Best Selling', 'Country']
data = pd.read_csv(r'shopistores.csv', header=None, names=names, encoding='utf-8')
urls = list(data['Store Address'])
lst=os.listdir(r'D:\a\data')
temp_res=[]
for i in lst:
    temp=i[:-4]
    temp_res.append(temp)
res=[]
for i in urls:
    if i not in temp_res:
        res.append(i)
print(res)
print(len(res))

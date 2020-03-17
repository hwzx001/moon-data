import pandas as pd

names=['jsondata']
data=pd.read_csv(r'result-test.csv',header=None,names=names,encoding='utf-8')
cols=data['jsondata']
'''
keys=[]
for i in cols:
    tempkeys=eval(i).keys()
    for j in tempkeys:
        if j not in keys:
            keys.append(j)
'''
atts=['id', 'title', 'handle', 'description', 'published_at', 'created_at', 'vendor', 'type', 'tags', 'price', 'price_min', 'price_max', 'available', 'price_varies', 'compare_at_price', 'compare_at_price_min', 'compare_at_price_max', 'compare_at_price_varies', 'variants', 'images', 'featured_image', 'options', 'url', 'media']
def save_to_csv(shop_list):
    data = pd.DataFrame(shop_list)
    data.to_csv('parse-json-result.csv', mode='a', index=False, sep=',', header=False,encoding='utf-8')

if __name__ == '__main__':
    names = ['jsondata']
    data = pd.read_csv(r'result-test.csv', header=None, names=names, encoding='utf-8')
    cols = data['jsondata']
    res=[]
    for i in cols:
        temp_col=[]
        tempdict = eval(i)
        for j in atts:
            if  j in tempdict.keys():
                temp_col.append(tempdict[j])
            else:
                temp_col.append('NULL')
        res.append(temp_col)
    save_to_csv(res)





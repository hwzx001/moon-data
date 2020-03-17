import requests
import json
import pandas as pd

def get_json_data(raw_url):
    url=raw_url+'.js'
    try:
        webdata=requests.get(url).text
        data=json.loads(webdata)
    except:
        return ''
    else:
        return data

def save_to_csv(shop_list,filename):
    data = pd.DataFrame(shop_list)
    data.to_csv(filename+'.csv', mode='a', index=False, sep=',', header=False,encoding='utf-8')

def test(filename):
    f=open(filename,'r',encoding='utf-8')
    urls=f.read().split('\n')
    res=[]
    count=0
    for i in urls:
        temp=get_json_data(i)
        if temp!='':
            res.append([temp])
            print(temp)
        else:
            count+=1
    print('num of products:',len(urls)-1)
    print('num of test sucess:',len(res))
    save_to_csv(res,filename+'-test')

#url=r'https://colourpop.com/products/blending-sponge?view=json'
#url='https://colourpop.com/products/flexitarian?view=json'
#url='https://jeffreestarcosmetics.com/products/im-royalty.js'
#url='https://www.fashionnova.com/products/cap-sleeve-peplum-dress-black-gold.json'
#url='https://www.reddress.com/products/leading-role-silver-clutch?view=swatch'
#url='https://www.cupshe.com/products/copy-of-gift-card-1.js'
#f=open('result.txt')
#urls=f.read().split('\n')

if __name__ == "__main__":
    test('3dfuel.com.csv')

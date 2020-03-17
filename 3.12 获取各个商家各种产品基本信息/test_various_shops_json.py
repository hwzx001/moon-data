import requests
import json
import pandas as pd

def get_json_data(raw_url):
    url=str(raw_url)+'.js'
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

def test():
    f=open('result.txt','r',encoding='utf-8')
    urls=f.read().split('\n')
    res=[]
    #lenurls=len(urls)
    lenurls=1000
    for i in range(lenurls):
        temp=get_json_data(urls[i])
        if temp!='':
            res.append([temp])
            #print(temp)
    #print('num of urls:',len(urls)-1)
    print('num of test sucess:',len(res))
    save_to_csv(res,'result-test')

if __name__ == "__main__":
    test()
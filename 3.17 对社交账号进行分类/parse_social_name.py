import pandas as pd
def parse(data):
    res=[]
    temp=str(data).split(',')
    res.append(temp[0])
    if len(temp)==1:
        res.extend(['--']*len(social_keys))
    else:
        for i in social_keys:
            index=find_str(i,temp)
            if index==-1:
                res.append('--')
            else:
                res.append(temp[index])
    return res

def find_str(temp,data):
    # temp 为子串，data为集合
    for i in range(1, len(data)):
        if data[i].find(temp) != -1:
            return i
    return -1

def save_to_csv(res):
    data = pd.DataFrame(res)
    data.to_csv('socialname.csv', mode='a', index=False, sep=',', header=names, encoding='utf-8')
names=['url','amazon', 'boards', 'businessinsider', 'citiesocial', 'cyrillcase', 'decathlon-united', 'desk', 'facebook', 'fleshjack', 'instagram', 'instyle', 'livechatinc', 'mailchi', 'pinterest', 'reddit', 'reddress', 'shopperapproved', 'snapchat', 'spigen', 'stevemadden', 'tiktok', 'twitter', 'vimeo', 'wsj', 'youtube']

social_keys=['amazon', 'boards', 'businessinsider', 'citiesocial', 'cyrillcase', 'decathlon-united', 'desk', 'facebook', 'fleshjack', 'instagram', 'instyle', 'livechatinc', 'mailchi', 'pinterest', 'reddit', 'reddress', 'shopperapproved', 'snapchat', 'spigen', 'stevemadden', 'tiktok', 'twitter', 'vimeo', 'wsj', 'youtube']
if __name__ == '__main__':
    res = []
    f = open('SocialInformation.csv', 'r', encoding='utf-8')
    s = f.read().split('\n')
    f.close()
    for i in s:
        temp=parse(i)
        res.append(temp)
    save_to_csv(res)
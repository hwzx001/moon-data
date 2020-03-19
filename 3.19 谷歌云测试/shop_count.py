import os
import pandas as pd
import matplotlib.pyplot as plt
import math
def count_shop(filename):
    names = ['url']
    data = pd.read_csv(filename, header=0, names=names, encoding='utf-8')
    s=data['url']
    return len(s)
if __name__ == '__main__':
    os.chdir(r'C:\Users\59103\Desktop\实习\3.11\data')
    lst=os.listdir()
    res=[]
    for i in lst:
        res.append(count_shop(i))
    ser_data = pd.Series(data=res)
    bin = [i for i in range(0, 10000, 50)]
    sel = pd.cut(ser_data, bin)
    pd.value_counts(sel)
    s = pd.DataFrame(pd.value_counts(sel))
    s.to_csv('count.csv', mode='a', index=True, sep=',', encoding='utf-8')


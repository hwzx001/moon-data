


if __name__ == "__main__":
    lst=open(r'D:\a\Shopify Store Leads\newdata.txt','r',encoding='utf-8').read().split('\n')
    cmplst=open('data.txt','r',encoding='utf-8').read().split('\n')
    dictcmp={}
    for i in lst:
        if len(i)>0:
            key=len(i)
            frist=str(i)[0]
            if key not in dictcmp:
                dictcmp[key]={}
                dictcmp[key][frist]=[i]
            else:
                if frist not in dictcmp[key].keys():
                    dictcmp[key][frist]=[i]
                else:
                    dictcmp[key][frist].append(i)
                

    res=open('res.txt','w',encoding='utf-8')
    for i in cmplst:
        temp=len(i)
        if temp not in dictcmp.keys():
            res.write(i)
            res.write('\n')
        else:
            frist_letter=str(i)[0]
            if frist_letter not in dictcmp[temp].keys() :
                res.write(i)
                res.write('\n')
            elif frist_letter  in dictcmp[temp].keys() and i not in  dictcmp[temp][frist_letter]:
                res.write(i)
                res.write('\n')
    res.close()
   
    
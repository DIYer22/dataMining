# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from __future__ import unicode_literals

def log(d):
    show_len = 20
    if isinstance(d,list):
        for i in d:
            strr = str(i)
            if len(strr) > show_len:
                print strr[:show_len] + '...'
            else:
                print strr
        return
            
    if isinstance(d,dict):
        for i in d:
            strr = str(i)+' = '+str(d[i])
            if len(strr) > show_len:
                print strr[:show_len] + '...'
            else:
                print strr          
        return
    print d


min_sup = 0.01
min_conf = 0.5
path = './retail2.dat'

f = open(path, 'r')
db = f.readlines()
f.close()



db = map(lambda strr:map(lambda x:int(x), strr[:-1].split(' ')[:-1]), db)


#min_sup = 0.5
#db = [
#[1,3,4],
#[2,3,5],
#[1,2,3,5],
#[2,5]]

min_sup *= len(db)
dic = {}  # 记录it 频率
dicc = {}  # 记录所有频繁项集
min_f = []  # 记录最小边缘频繁项集
a_r = []  # 记录边缘强关系
for items in db:
   for item in items:
       dic[item] = 1 if item not in dic else dic[item] + 1


# 删除小于 min_sup 的item
[dic.pop(k) if not dic[k]>= min_sup else None for k in dic.keys()]
l1 = []
for k in dic:
    l1 += [(k,)]
    dicc[(k,)] = dic[k]




def _del(l, c):  # 根据C(k+1) 删去非边缘频繁项集
    n = len(c)
    for i in range(n):
        t = c[:i]+c[i+1:]
#        print l,t,c
        if t in l:
            l.remove(t)
    
def gen_k(l):
    '''l 输入Lk 生成 C(k+1) 
       及记录最小边缘频繁项集 min_f
    '''
    n = len(l[0])    
    lenn = len(l)
    d = {}
    for i in range(lenn-1):
        for j in range(i+1 ,lenn):  # 自连接
            
            sett = set(l[i]+l[j])
            if len(sett) != n+1:
                continue
            _l = list(sett)
            _l.sort()
            sett = tuple(_l)
            if sett not in d:
                d[sett] = [1]*(n+1)  # 用于标记是否缺失
            for it in l[i]:
                if it in l[j]:
                    _l.remove(it)  # 删除相同的k-2个元素
            for it in _l:
                d[sett][sett.index(it)] = 0
            
    for key in d.keys():
        if sum(d[key]) != 0:
            d.pop(key)
    return d.keys()
            

def its_belong_t(its, t):
    summ = 0
    for it in its:
        if it not in t:
            summ += 1
    return not summ

def c_n(n, listt, l, b, r):  # 递归生成全排列
    ''' n 剩余选择数量
        listt 全排列目标
        b 起始值
        l 临时记录
    '''
    if n == 0:  # 生成关系并计算支持度 
        r.append(tuple(l))
        return
    for i in range(b, len(listt)-n+1):
        l += [listt[i]]
        c_n(n-1, listt, l, i+1,r)
        l.pop()
    return 

def combination(its):  # 对边缘频繁项集 递归生成排列
    n = len(its)
    l = []
    if n == 1:
        return (its)
    for lenth in range(1, n+1):
        c_n(lenth, its, [],0,l)
    return l
    
    

l = l1
while 1:  
    c = gen_k(l)  # 生成候选集 C(k+1)
    if len(c) == 0 :
        break
    print 'k=%d,candidate=%d'%(len(c[0]),len(c))
    min_l = l[:]  # 精简l 用于求最小边缘频繁项集
    d = {}
    for t in db:  # 对每条事务t 计数 候选集内关系出现次数        
        t = filter(lambda x:x in dic, t)
#        for its in c:     
#            if its_belong_t(its, t):  # 若属于 则
#                d[its] = 1 if its not in d else d[its]+1
        if len(t) < len(c[0]):
            continue
        tup=[]
        c_n(len(c[0]), t, [],0,tup)
#        print 'tup',tup
        for its in tup:
            d[its] = 1 if its not in d else d[its]+1
    l = [key if d[key] >= min_sup else None for key in d]
    l = filter(None, l)
    for it in l:
        dicc[it]=d[it] 
        _del(min_l, it)
    [min_f.append(i) for i in min_l]
    if len(l) == 0:
        break

frequent = filter(lambda x:len(x)!=1 ,dicc.keys())

print 'len', len(dicc)
# 由最小边缘频繁项集求强关系






#
#
def c_n2(n, listt, l=[], b=0):  # 递归生成最小边缘强关系
    ''' n 剩余选择数量
        listt 全排列目标
        b 起始值
        l 临时记录
    '''
    if n == 0:  # 生成关系并计算支持度 
        a = tuple(l)
        print listt, a
        sup = float(dicc[tuple(listt)]) / dicc[a]
        b = filter(lambda x:x not in l, listt)
        if sup >= min_conf:  
            b = tuple(b)
            a_r.append((a,b))
#            print 'add:', (a,b)
        else:
#            print 'f(%s)'%str(b)
            its_to_ar(b)
        return
    for i in range(b, len(listt)-n+1):
        l += [listt[i]]
        c_n2(n-1, listt, l, i+1)
        l.pop()
    return 

def its_to_ar(its):  # 对边缘频繁项集 递归生成强规则
    n = len(its)
    if n == 1:
        return
    for lenth in range(1, n):
        c_n2(lenth, its, [])


for its in min_f:
    its_to_ar(its)


# 打印所有强关系
for ar in a_r:
    strr = ''
    for i in ar[0]:
        strr += str(i) + ' '
    strr += '=> '
    for i in ar[1]:
        strr += str(i) + ' '
    print strr

#print 'dic=', len(dic)
#print 'dicc=', len(dicc)
#print 'min_f=', len(min_f)
#print 'a_r=', len(a_r)
#
#print 'resoult',dicc.keys()
# 

print 'min Association Rules', len(a_r)
print 'frequent itemset', len(dicc)

#myy = my[:]
#
#
#
#for i in my[:]:
#    if i in min_f:
#        min_f.remove(i)
#        my.remove(i)
#
#log(my)
#print '\n_f'
#log(min_f)
#
#my = myy



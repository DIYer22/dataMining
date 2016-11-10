# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from __future__ import unicode_literals

def log(d):
    show_len = 40
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

MAX_L = 22
def p_tree(t,level = 0):
    if level > MAX_L:
        return
    for i in t:
        if  not isinstance(i,int):
            continue
        print level*'| '+'%d :%d'%(i, t[i]['c'])
        p_tree(t[i],level+1)
        

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




root = {}
record = {}
def add_tree(its, tree, count, record, dic):
    ''' 
    将 count个 items 加入 tree
    
    如果record_flag为True 则记录
    tree 的结构
    s self
    f father
    c count
    [\d] child
    '''
    its = filter(lambda x: x in dic, its)
    its.sort(lambda x, y:  1 if dic[x] < dic[y] else -1 )
    for it in its:
        if it not in tree:
            tree[it] = {}
            tree[it]['f'] = tree
            tree[it]['s'] = it
            record[it]=[tree[it]] if it not in record else record[it]+[tree[it]]
        tree = tree[it]
        tree['c'] = count if 'c' not in tree else tree['c'] + count

    


for items in db:
    add_tree(items, root, 1, record, dic)


#print 'dic',
#log(dic)

print '\nrecord',log('')

#p_tree(root)

fp_l = dic.items()
fp_l.sort(lambda x, y: 1 if x[1]<y[1] else -1)


def creat_its(t):
    l=[]
    while 1:
        t = t['f']
        if 'f' not in t:
            break
        l += [t['s']]
        
    return l[::-1]

dicc ={}

def is_singl_tree(t):
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
            return [its]
        for lenth in range(1, n+1):
            c_n(lenth, its, [],0,l)
        print 'its',its,l
        return l

        
    l = []
    root = t
    while 1:
        tmp = filter(lambda x:isinstance(x, int), t.keys())
        n = len(tmp)
        if n != 1 and n != 0:
#            print l,p_tree(root)
            return None
        if n == 0 :
            
            if 'f' in t:
#                print 'tmp',l
#                print tmp,root.keys(),l,combination(l)
                return [list(i) for i in combination(l)]
            return None
        l += tmp
        
        t=t[tmp[0]]
        
        
    
    
    
def header_to_db(fp_list, record):
    l = []
#    print 'fp',fp_list
    for it in fp_list[::-1]:
        it = it[0]
        db = []
        for t in record[it]:
            db += [(creat_its(t), t['c'])]
#        print 'db',db
        dic = {}
        for items in db:
           for item in items[0]:
               dic[item] = items[1] if item not in dic else dic[item] + items[1]
        # 删除小于 min_sup 的item
        [dic.pop(k) if not dic[k]>= min_sup else None for k in dic.keys()]

        t = {'s':'root'}
        header = {}
        for its in db:
            add_tree(its[0], t, its[1], header, dic)
        r = is_singl_tree(t)
#        print 'it',it,r,dic
        if r != None:  # 若已经是 single 了 则不必继续递归
#            print 'r',r
            l += [i+[it] for i in r]+[[it]]
#            print 'add',[i+[it] for i in r]
            continue
        
        fp_l = dic.items()
        fp_l.sort(lambda x, y: 1 if x[1]<y[1] else -1)

        r = header_to_db(fp_l, header)
        l += [i+[it] for i in r]+[[it]]
    return l



#for it in fp_l[::-1]:
#    f(it[0])
r = header_to_db(fp_l, record)

#print 'resoult',r
 
print 'frequent itemset', len(r)
 
 






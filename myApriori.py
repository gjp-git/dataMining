#coding=utf-8                        # 全文utf-8编码
import sys
from collections import defaultdict

def apriori(Dpre, minSup):
    
    #转换为set表示
    D = map(set,Dpre)
    n = len(D)
    LS = []
    #构建C1
    C1 = {}
    for dItem in D:
        for item in dItem:
            if item in C1:
                C1[item] += 1
            else:
                C1[item] = 1
    
    #计算L1
    L1 = {}
    for k,v in C1.items():
        if v*1.0/n >= minSup:
            L1[k] = v
    LS.append(L1)
    
    k=2;

    while len(LS[k-2])>0:
        preL = LS[k-2].keys()
        preLLen = len(preL)
        #构建Ck
        currentC = set()
        #自连接
        for i in range(preLLen-1):
            for j in range(i+1,preLLen):
                l1 = preL[i]
                l2 = preL[j]
                if l1[:k-3] == l2[:k-3] and l1[k-2] != l2[k-2]:
                    if l1[k-2] < l2[k-2]:
                        currentC.add(""+l1[:]+l2[k-2])
                    else:
                        currentC.add(""+l2[:]+l1[k-2])

        #剪枝
        currentCAfterCut = set(currentC)
        for CItem in currentC:
            Ckmin1Items = []
            for i in range(k):
                Ckmin1Items.append(CItem[:i]+CItem[i+1:])

            for Ckmin1Item in Ckmin1Items:
                if not(Ckmin1Item in preL):
                    currentCAfterCut.remove(CItem)
                    break

        #计数
        Ck = defaultdict(int)
        for dItem in D:
            for cItem in currentCAfterCut:
                if set(cItem).issubset(dItem):
                    Ck[cItem] += 1
        Lk = {}
        for item,num in Ck.items():
            if num*1.0/n >= minSup:
                Lk[item] = num

        LS.append(Lk)
        k += 1
    return LS

def generateRules(res,min_conf):
    result = {}
    support = {}
    for Lk in res:
        for k,v in Lk.items():
            support[k] = v

    for i in range(1,len(res)):
        for l in res[i]:
            #每个频繁项集
            #规则后件，用于生成新规则
            RuleBackward = []
            
            #求1项集后件的关联规则
            R1B = []
            for lItem in l:
                lTemp = ""
                for x in l:
                    if not x in lItem:
                        lTemp = lTemp+x
                
                conf = support[l]*1.0/support[lTemp]
                
                if conf >= min_conf:
                    result[lTemp+"->"+lItem] = conf
                    R1B.append(lItem)
                    
            RuleBackward.append(R1B)
            k = 2
            
            while len(RuleBackward[k-2])>0 and k<len(l):
                RkBPre = RuleBackward[k-2]
                RkBLen = len(RkBPre)
                RkB = []

                for i in range(RkBLen-1):
                    for j in range(i+1,RkBLen):
                        l1 = RkBPre[i]
                        l2 = RkBPre[j]
                        lnew = ""
                        #自连接
                        if l1[:k-3] == l2[:k-3] and l1[k-2] != l2[k-2]:
                            if l1[k-2] < l2[k-2]:
                                lnew = l1[:]+l2[k-2]
                            else:
                                lnew = l2[:]+l1[k-2]
                                
                            #求前件
                            lTemp = ""
                            for x in l:
                                if not x in lnew:
                                    lTemp = lTemp + x
                            
                            conf = support[l]*1.0/support[lTemp]
                            if conf >= min_conf:
                                result[lTemp+"->"+lnew] = conf
                                RkB.append(lnew)
                                
                RuleBackward.append(RkB)
                k += 1
    return result

    
if __name__ =='__main__':   
    #D = ['125','24','23','124','13','23','13','1235','123','0']
    D = ['ace','bd','bc','abcd','ab','bc','ab','abce','abc','ace']
    F = apriori(D, 0.2)
    print '\nfrequent itemset:\n', F
    G = generateRules(F,0.5)
    for k,v in G.items():
        print k," conf:",v
#coding=utf-8

import myApriori as ap
from collections import defaultdict
import itertools
import copy 

class TreeNode(object):
    #四个属性 nodeName count parent children
    def __init__(self, nodeName, parent, count = 1):
        self.nodeName = nodeName
        self.parent = parent
        self.count = count
        self.children = set()
        
    def addChildren(self,child):
        if not child in self.children:
            self.children.add(child)
            
    def removeChildren(self,child):
        if child in self.children:
            self.children.remove(child)
            
    def addCount(self,num = 1):
        if isinstance(num,int):
            self.count += num
            
def FPGrowth(D,min_sup):
    n = len(D)
    
    C1 = defaultdict(int)
    for DItem in D:
        for di in DItem:
            C1[di] += 1
    
    L1Dict = filterSup(C1,min_sup,n)
    #排序
    #L1 = [i[0] for i in sorted(L1Dict.iteritems(),key=lambda d:d[1], reverse = True)]
    L1 = [i[0] for i in sorted(sorted(L1Dict.iteritems(),key=lambda d:d[0]),key=lambda d:d[1], reverse = True)]
    #初始化项头表
    itemDict = {}
    for lItem in L1:
        itemDict[lItem] = {}
        itemDict[lItem]['sup'] = L1Dict[lItem]
        itemDict[lItem]['itemSet'] = set()
    
    #创建根节点null
    nullNode = TreeNode('null',TreeNode('nullParent',None))
    
    for DItem in D:
        t = []
        for lItem in L1:
            if lItem[0] in DItem:
                t.append(lItem[0])
                
        insertFP(t,nullNode,itemDict)
    
    LS = {}
    SearchFP(nullNode,[],n,min_sup,itemDict,L1,LS)
    return LS

#获得频繁项集
def filterSup(d,min_sup,n):
    result = {}
    for k,v in d.iteritems():
        if v*1.0/n >= min_sup:
            result[k] = v
    return result

def insertFP(t,rootNode,itemDict):
    if len(t)>0:
        #取排好顺序的事务的第一项
        firstNodeName = t[0]
        hasChild = False
        thisNode = None
        for node in rootNode.children:
            #有节点，支持度+1
            if firstNodeName == node.nodeName:
                node.addCount()
                thisNode = node
                hasChild = True
                break
        #没有节点，创建
        if not hasChild:
            thisNode = TreeNode(firstNodeName,rootNode)
            itemDict[firstNodeName]['itemSet'].add(thisNode)
            rootNode.addChildren(thisNode)
        
        insertFP(t[1:],thisNode,itemDict)

def SearchFP(rootNode,a,n,min_sup,itemDict,itemList,LS):
    if not checkBranch(rootNode):
        nodeDict = itemDict
        combList = getSubset(itemList)
        #print 'itemList',itemList
        #print 'combList',combList
        for combItems in combList:
            sup = n+1
            for combItem in combItems:
                sup = min(nodeDict[combItem]['sup'],sup)
            
            comb = list(combItems)
            comb.extend(a)
            comb.sort()
            #print 'comb',comb
            LS[reduce(lambda x,y:x+y,comb)] = sup
    else:
        for item in itemList[::-1]:
            thisa = []
            thisa.append(item)
            thisa.extend(a)
            thisSup = itemDict[item]['sup']
            
            if thisSup*1.0/n >= min_sup:
                LS[reduce(lambda x,y:x+y,sorted(thisa))] = thisSup
            
            thisItemDict = copy.deepcopy(itemDict)
            thisItemList = itemList[:itemList.index(item)]
            thisNullNode = list(thisItemDict[item]['itemSet'])[0]
            
            #获得深copy的新树的根节点，通过新树构造条件FP树
            while thisNullNode.nodeName != 'null':
                thisNullNode = thisNullNode.parent
            
            #除项尾sup值初始为0
            for it in thisItemList:
                map(initSup,thisItemDict[it]['itemSet'])
                thisItemDict[it]['sup']=0
            
            #计算条件FP树的sup值
            for itemNode in thisItemDict[item]['itemSet']:
                tempNode = itemNode.parent
                itemCount = itemNode.count
                while tempNode.nodeName != 'null':
                    tempNode.addCount(itemCount)
                    thisItemDict[tempNode.nodeName]['sup'] += itemCount
                    tempNode = tempNode.parent
                #删除项头表项尾
                itemNode.parent.children.remove(itemNode)
                itemNode.parent = None
                
            #删除项头表项尾
            for it in itemList[itemList.index(item):]:
                thisItemDict.pop(it)
            
            #删除0项和小于min_sup的项
            for it in thisItemList:
                for niter in thisItemDict[it]['itemSet']:
                    if niter.count*1.0/n < min_sup:
                        thisItemDict[it]['sup'] -= niter.count
                        niter.parent.children.remove(niter)
                        niter.parent = None
            
            thisItemList = [i for i in thisItemList if thisItemDict[i]['sup']!=0] 
            
            if len(thisNullNode.children)>0:
                #print 'itemsearch',item,thisItemList
                SearchFP(thisNullNode,thisa,n,min_sup,thisItemDict,thisItemList,LS)
    
def checkBranch(node):
    if len(node.children)>1:
        return True
    elif len(node.children)==0:
        return False
    else:
        return checkBranch(list(node.children)[0])

        
def getNodeSup(node):
    nodeDict = {}
    if len(node.children)==0:
        return {nodeName:count}
    else:
        for child in node.children:
            temp = getNodeSup(child)
            nodeDict.update(temp)
    return nodeDict
    
#获得除空集外所有子集
def getSubset(s):
    result = []
    for i in range(1,2**len(s)):
        t=''
        for j in range(0,len(s)):
            if i&(2**j) >0:
                t=t+s[j]
        result.append(t)
    return result

    
def cutTree(node):
    if node.count == 0:
        node.parent.children.remove(node)
        node.parent = None
        return
    elif len(node.children)==0:
        return
    else:
        for child in node.children:
            cutTree(child)
def cutItem(node,item,newNode,thisItemList):
    if len(node.children)==0:
        return
    else:
        for child in node.children:
            if child.nodeName != item:
                newChild = TreeNode(child.nodeName,newNode,0)
                newNode.addChildren(newChild)
                thisItemList[child.nodeName]['itemSet'].add(newChild)
                cutItem(child,item,newChild,thisItemList)
def initSup(node):
    node.count = 0
def showNode(node):
    if len(node.children)==0:
        print node.nodeName," ",node.parent.nodeName," ",node.count
    else:
        print node.nodeName," ",node.parent.nodeName," ",node.count," ",map(lambda d:d.nodeName,node.children)
        for child in node.children:
            showNode(child)
        
if __name__ =='__main__':   
    D = ['125','24','23','124','13','23','13','1235','123','0']
    #D = ['ace','bd','bc','abcd','ab','bc','ab','abce','abc','ace']
    F = FPGrowth(D, 0.2)
    print '\nfrequent itemset:\n', F
    #G = ap.generateRules(F,0.5)
    #for k,v in G.items():
    #    print k," conf:",v
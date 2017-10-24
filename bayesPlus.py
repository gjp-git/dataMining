# -*- coding: utf-8 -*-

import pandas as pd
from collections import defaultdict
import math

class TreeNode(object):
	def __init__(self, nodeName):
		self.nodeName = nodeName
		self.link = set()
		self.parent = None
		self.children = set()

			
def bayesPlus(data,attrs,cls,sample):
	res = {}
	n = len(data)
	clsProb = dict(data.groupby(cls).size()*1.0/n)
	attrsDict = {}
	attrsProb = {}
	IList = []
	
	for attrsItem in attrs:
		attrsDict[attrsItem] = list(data.groupby(attrsItem).size().index)
		attrsProb[attrsItem] = defaultdict(int)
		for clsItem in clsProb:
			#防止分类下没有该属性值，取值时keyerror
			attrsProb[attrsItem][clsItem] = defaultdict(int)
			attrsProb[attrsItem][clsItem].update(dict(data[data[cls]==clsItem].groupby(attrsItem).size()/len(data[data[cls]==clsItem])))
	
	#计算条件互信息
	for i in range(len(attrs)-1):
		for j in range(i+1,len(attrs)):
			I = 0
			attr1 = attrs[i]
			attr2 = attrs[j]
			for clsItem in clsProb:
				for attr1Item in attrsDict[attr1]:
					for attr2Item in attrsDict[attr2]:
						pxyz = len(data.loc[(data[attr1]==attr1Item)&(data[attr2]==attr2Item)&(data[cls]==clsItem)])*1.0/n
						if pxyz!=0:
							I += pxyz*math.log(pxyz/clsProb[clsItem]/(attrsProb[attr1][clsItem][attr1Item]*attrsProb[attr2][clsItem][attr2Item]),2)
			IList.append({'attr1':attr1,'attr2':attr2,'I':I})
	print IList
	
	#创建根节点
	rootNode = TreeNode(cls)
	rootNode.parent = TreeNode('none')
	#构造有向图
	createTree(IList,attrs,rootNode)
	#根据有向图计算概率
	for k,v in clsProb.iteritems():
		#前置条件 包括分类和图中的前置条件
		prefix = {}
		prefix[cls] = k
		prob = v
		res[k] = prob*traceTree(rootNode,sample,prefix,cls)
	
	#print res
	#返回概率最大的类标签
	return reduce(lambda x,y:x if res[x]>res[y] else y,res)
		
	
def createTree(list,point,rootNode):
	#对条件互信息排序 从大到小取
	edge = sorted(list,key = lambda x:x['I'],reverse = True)
	pointSet = set()
	edgeNum = 0
	#记录端点 防止形成回路
	pointDict = {}
	for pItem in point:
		pointDict[pItem] = TreeNode(pItem)
	for tempDict in edge:
		#取n-1条边
		if edgeNum == len(point):
			break
		#判断两端点是否同时在端点集合中，都在即形成了回路
		if not ((tempDict['attr1'] in pointSet) and (tempDict['attr2'] in pointSet)):
			pointSet.add(tempDict['attr1'])
			pointSet.add(tempDict['attr2'])
			edgeNum += 1
			pointDict[tempDict['attr1']].link.add(pointDict[tempDict['attr2']])
			pointDict[tempDict['attr2']].link.add(pointDict[tempDict['attr1']])
	#根节点任取一点作为下一节点
	rootNode.link.add(pointDict[attrs[0]])
	pointDict[attrs[0]].link.add(rootNode)
	#将无向图转化为有向图
	setDirction(rootNode)
	#showNode(rootNode)

def setDirction(rootNode):
	for item in rootNode.link:
		rootNode.children.add(item)
		item.link.remove(rootNode)
		item.parent = rootNode
		setDirction(item)

def traceTree(rootNode,sample,prefix,cls):
	thisProb = 1
	for item in rootNode.children:
		thisPrefix = {}
		prefixProb = ''
		allProb = '(data[\''+item.nodeName+'\']=='+'\''+sample[item.nodeName]+'\''+')&'
		for k,v in prefix.iteritems():
			prefixProb += ('(data[\''+k+'\']=='+'\''+v+'\''+')&')
		
		prefixProb = prefixProb[:-1]
		allProb += prefixProb
		if len(data.loc[eval(prefixProb)])==0:
			return 0
		prob = len(data.loc[eval(allProb)])*1.0/len(data.loc[eval(prefixProb)])
		thisProb *= prob
		thisPrefix[cls] = prefix[cls]
		thisPrefix[item.nodeName] = sample[item.nodeName]
		#print prob,thisPrefix
		thisProb *= traceTree(item,sample,thisPrefix,cls)
	return thisProb

#测试方法 打印树结构
def showNode(node):
	if len(node.children)==0:
		print node.nodeName," ",node.parent.nodeName
	else:
		print node.nodeName," ",node.parent.nodeName," ",map(lambda d:d.nodeName,node.children)
		for child in node.children:
			showNode(child)
			
if __name__ =='__main__': 
	cols = ['age','income','student','credit','buyComputer']
	data = pd.read_table('D:/$Python data analysis/DataMining/SSet.txt',sep=',',header=0,names=cols,engine = 'python')
	attrs = ['age','income','student','credit']
	cls = 'buyComputer'
	sample = {'age':'31-40','income':'middle','student':'F','credit':'high'}
	print cls,'?:',bayesPlus(data,attrs,cls,sample)
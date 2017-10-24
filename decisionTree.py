# -*- coding: utf-8 -*-

import math
import pandas as pd
from collections import defaultdict

class TreeNode(object):
	def __init__(self):
		self.children = {}
		
	def addChildren(self,key,child):
		self.children[key] = child

def decisionTree(data,attrs,cls,sample):
	rootNode = generateTree(data,attrs,cls)
	'''
	a = TreeNode()
	a.nodeName = 'None'
	rootNode.parent = a
	showNode(rootNode)
	'''
	thisNode = rootNode
	while len(thisNode.children)!=0:
		thisNode = thisNode.children[sample[thisNode.nodeName]]
		
	return thisNode.nodeName

def getGainMaxAttr(data,attrs,cls):
	clsSize = data.groupby(cls).size()
	clsProbDict = dict(clsSize*1.0/len(data))
	n = len(data)
	
	GainDict = {}
	attrsDict = {}
	#print clsProbDict
	EC = 0 
	for k,v in clsProbDict.iteritems():
		EC -= v*math.log(v,2)
	#print 'EC:',EC
	for attrsItem in attrs:
		ECA = 0
		attrsDict[attrsItem] = list(data.groupby(attrsItem).size().index)
		Sij = defaultdict(int)
		Sj = defaultdict(int)
		Sij.update(data.groupby([cls,attrsItem]).size().to_dict())
		Sj.update(data.groupby(attrsItem).size().to_dict())
		for attr in attrsDict[attrsItem]:
			temp = 0
			for clsItem in clsProbDict:
				if Sij[(clsItem,attr)]==0:
					continue
				temp += Sij[(clsItem,attr)]*1.0/Sj[attr]*math.log(Sij[(clsItem,attr)]*1.0/Sj[attr],2)
			ECA -= Sj[attr]*1.0/n*temp
		GainDict[attrsItem] = EC - ECA
	#print GainDict
	return reduce(lambda x,y:x if GainDict[x]>GainDict[y] else y,GainDict)
	
def generateTree(data,attrs,cls):
	#创建决策树根节点
	rootNode = TreeNode()
	if len(data.groupby(cls).size()) == 1:
		rootNode.nodeName = data.groupby(cls).size().index[0]
		return rootNode
	if len(attrs) == 0:
		temp = data.groupby(cls).size().to_dict()
		rootNode.nodeName = reduce(lambda x,y:x if temp[x]>temp[y] else y,temp)
		return rootNode
		
	attr = getGainMaxAttr(data,attrs,cls)
	#print attr
	rootNode.nodeName = attr
	
	for item in data[attr].drop_duplicates().values:
		dataSubset = data[data[attr] == item]
		if len(dataSubset) == 0:
			classNode = TreeNode()
			temp = dataSubset.groupby(cls).size().to_dict()
			classNode.nodeName = reduce(lambda x,y:x if temp[x]>temp[y] else y,temp)
			classNode.parent = rootNode
			rootNode.addChildren(item,classNode)
		else:
			attrsSubset = list(attrs)
			attrsSubset.remove(attr)
			#print 'attrsSubset',attrsSubset
			classNode = generateTree(dataSubset,attrsSubset,cls)
			classNode.parent = rootNode
			rootNode.addChildren(item,classNode)
			
	return rootNode
	
#测试方法 打印树结构
def showNode(node):
	if len(node.children)==0:
		print node.nodeName," ",node.parent.nodeName
	else:
		print node.nodeName," ",node.parent.nodeName," ",node.children.keys()
		for k,child in node.children.iteritems():
			showNode(child)
			
if __name__ =='__main__': 
	cols = ['age','income','student','credit','buyComputer']
	data = pd.read_table('D:/$Python data analysis/DataMining/SSet.txt',sep=',',header=0,names=cols,engine = 'python')
	attrs = ['age','income','student','credit']
	cls = 'buyComputer'
	sample = {'age':'31-40','income':'middle','student':'F','credit':'high'}
	print cls,'?:',decisionTree(data,attrs,cls,sample)
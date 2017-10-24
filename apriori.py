#coding=utf-8                        # 全文utf-8编码
import sys

def apriori(Dpre, minSup):
	
	'''频繁项集用keys表示，
	key表示项集中的某一项，
	cutKeys表示经过剪枝步的某k项集。
	C表示某k项集的每一项在事务数据库D中的支持计数
	'''
    #转换为列表表示
	D = []
	for d in Dpre:
		temp=[]
		for item in d:
			temp.append(item)
		D.append(temp)
	
	#构建C1
	C1 = {}
	for dItem in D:
		for item in dItem:
			if item in C1:
				C1[item] += 1
			else:
				C1[item] = 1

	print C1
    
	_keys1 = C1.keys()

	keys1 = []
	for i in _keys1:
		keys1.append([i])

	n = len(D)
	cutKeys1 = []
	for k in keys1[:]:
		if C1[k[0]]*1.0/n >= minSup:
			cutKeys1.append(k)
	
	cutKeys1.sort()


	keys = cutKeys1
	all_keys = []
	while keys != []:
		C = getC(D, keys)
		cutKeys = getCutKeys(keys, C, minSup, len(D))
		for key in cutKeys:
			all_keys.append(key)
		keys = aproiri_gen(cutKeys)

	return all_keys

def getC(D, keys):
	'''对keys中的每一个key进行计数'''
	C = []
	for key in keys:
		c = 0
		for T in D:
			have = True
			for k in key:
				if k not in T:
					have = False
			if have:
				c += 1
		C.append(c)
	return C

def getCutKeys(keys, C, minSup, length):
	'''筛选'''
	lkeys = []
	for i, key in enumerate(keys):
		if float(C[i]) / length >= minSup:
			lkeys.append(key)
	return lkeys



def keyInT(key, T):
	'''判断项key是否在数据库中某一元组T中'''
	for k in key:
		if k not in T:
			return False
	return True


def aproiri_gen(keys1):
	'''连接步'''
	keys2 = []
	newkeys = []
	n = len(keys1[0])
	for k in keys1:
		if k[n-1] not in newkeys:
			newkeys.append(k[n-1])
	
	for k in keys1:
		for i in newkeys:
			temp = list(k)
			if i not in k:
				temp.append(i)
				temp.sort()
				if temp not in keys2:
					keys2.append(temp)
					
	'''剪枝'''

	return keys2
	
D = ['125','24','23','124','13','23','13','125','123','0']
F = apriori(D, 0.2)
print '\nfrequent itemset:\n', F
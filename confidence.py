# -*- coding: utf-8 -*-

def loadDataSet(Dpre):
	'''
	���룺�ַ�������
	���ܣ������򵥵����ݼ�
	�����dataset
	'''
	D = []
	for d in Dpre:
		temp=[]
		for item in d:
			temp.append(item)
		D.append(temp)
	return D

def createC1(dataset):
	'''
	���룺���ݼ�
	���ܣ���������[[1], [2], [3], [4], [5]]��C1�а�����Ԫ��Ϊ���ݼ��г��ֵ�Ԫ��
	�����C1
	'''
	C1 = []
	for transction in dataset:
		for item in transction:
			if not [item] in C1:
				C1.append([item])#ʹ���б���ΪC1Ԫ������Ϊ������Ҫʹ�ü��ϲ���
	C1.sort()
	return  map(frozenset,C1)

def scanDataSet(DataSet,Ck,minSupport):
	'''
	���룺DataSetӦΪÿ����¼��set�������ݣ��������ж��Ƿ������Ӽ���������Ck�е�ÿ���Ϊfrozenset�����ݣ��������ֵ�ؼ��֣�
		 CkΪ��ѡƵ�����minSupportΪ�ж��Ƿ�ΪƵ�������С֧�ֶȣ���Ϊ������
	���ܣ��Ӻ�ѡ����ҳ�֧�ֶ�support����minSupport��Ƶ���
	�����Ƶ�������returnList,�Լ�Ƶ�����Ӧ��֧�ֶ�support
	'''
	subSetCount = {}
	for transction in DataSet:#ȡ�����ݼ�dataset�е�ÿ�м�¼
		for subset in Ck:#ȡ����ѡƵ���Ck�е�ÿ���
			if subset.issubset(transction):#�ж�Ck����Ƿ������ݼ�ÿ����¼���ݼ����е��Ӽ�
				if not subSetCount.has_key(subset):
					subSetCount[subset] = 1
				else:
					subSetCount[subset] += 1
	numItem = float(len(DataSet))
	returnList =[]
	returnSupportData = {}
	for key in subSetCount:
		support = subSetCount[key]/numItem
		if support >= minSupport:
			returnList.insert(0,key)  
			returnSupportData[key] = support
	return returnList,returnSupportData

def createCk(Lk,k):
	returnList = []
	lenLk = len(Lk)
	for i in range(lenLk):
		for j in range(i+1,lenLk):
			L1 = list(Lk[i])[:k-2];L2 = list(Lk[j])[:k-2]
			L1.sort();L2.sort()
			if L1 == L2:#ֻ��ȡǰk-2��Ԫ����ȵĺ�ѡƵ����������Ԫ�ظ���Ϊk+1�ĺ�ѡƵ�������
				returnList.append(Lk[i] | Lk[j]) #ȡ����
	return returnList

def apriori(dataset,minSupport = 0.5):
	C1 = createC1(dataset)
	DataSet = map(set,dataset)
	print DataSet
	L1,returnSupportData = scanDataSet(DataSet,C1,minSupport)
	L = [L1]
	print L
	print "-----"
	k = 2
	while (len(L[k-2]) > 0):
		#����һʱ�̵�Ƶ���Lk-1����������γ���һʱ��û���ظ���Ƶ�������һʱ�̺�ѡƵ�����Ԫ�ظ��������һʱ�̵Ķ�1
		Ck = createCk(L[k-2],k)
		#�Ӻ�ѡƵ�����ѡ��֧�ֶȴ���minsupport��Ƶ���Lk
		Lk,supportLk = scanDataSet(DataSet,Ck,minSupport)
		#����Ƶ�������֧�ֶ���ӵ�returnSupportData�ֵ��м�¼������Ƶ���Ϊ�ؼ��֣�֧�ֶ�Ϊ�ؼ�������Ӧ����
		returnSupportData.update(supportLk)
		#��Ƶ�����ӵ��б�L�м�¼
		L.append(Lk)
		#��һ����Ƶ����е�Ԫ�ظ���
		k += 1
	return L, returnSupportData

#------------------�����������ɺ���--------------#
def generateRules(L,supportData,minConference = 0.7):
	#print "L",L
	#print "supportData",supportData
	bigRuleList = []
	for i in range(1,len(L)):
		for subSet in L[i]:
			H1 = [frozenset([item]) for item in subSet]
			if (i > 1):
				rulesFromConseq(subSet, H1, supportData, bigRuleList, minConference)
			else:
				calculationConf(subSet, H1, supportData,bigRuleList,minConference)
	return bigRuleList

def calculationConf(subSet, H, supportData,brl,minConference=0.7):
	prunedH = []
	for conseq in H:
		conf = supportData[subSet]/supportData[subSet - conseq]
	if conf >= minConference:
		print subSet-conseq,'-->',conseq,'conf:',conf
		brl.append((subSet-conseq,conseq,conf))
		prunedH.append(conseq)
	return prunedH

def rulesFromConseq(subSet, H, supportData, brl, minConference):
	m = len(H[0])
	#���Ƶ�����ÿ��Ԫ�ظ�������m+1,�������Էֳ�m+1��Ԫ���ڹ����ʽ�ұ���ִ��
	if (len(subSet) > (m+1)):
		#���ú���createCk���ɰ���m+1��Ԫ�صĺ�ѡƵ������
		Hm = createCk(H, (m+1))
		#����ǰ����subSet - Hm��--> �����Hm���Ŀ��Ŷȣ������ؿ��Ŷȴ���minConference�ĺ��
		Hm = calculationConf(subSet,Hm,supportData,brl,minConference)
		#����ѡ���������ֻ��һ������Ŀ��Ŷȴ�����С���Ŷȣ�������ݹ鴴������
		if (len(Hm) > 1):
			rulesFromConseq(subSet, Hm, supportData, brl, minConference)

#------------------�����������ɺ���end--------------#        
if __name__ =='__main__':        
	dataset = loadDataSet(['125','24','23','124','13','23','13','1235','123','0']) 
	dataset = loadDataSet(['ace','bd','bc','abcd','ab','bc','ab','abce','abc','ace'])
	L,returnSupportData = apriori(dataset,minSupport=0.2) 
	rule = generateRules(L, returnSupportData, minConference =0.5)
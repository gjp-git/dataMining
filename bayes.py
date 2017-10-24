# -*- coding: utf-8 -*-

import pandas as pd

def bayes(data,attrs,cls,sample):
    clsProb = dict(data.groupby(cls).size()*1.0/len(data))
    attrsProb = {}
    
    for attrsItem in attrs:
        attrsProb[attrsItem] = {}
        for clsItem in clsProb:
            attrsProb[attrsItem][clsItem] = dict(data[data[cls]==clsItem].groupby(attrsItem).size()/len(data[data[cls]==clsItem]))

    res = {}
    for clsItem in clsProb:
        res[clsItem] = clsProb[clsItem]
        for k,v in sample.iteritems():
            res[clsItem] *= attrsProb[k][clsItem][v]
    print res
    return reduce(lambda x,y:x if res[x]>res[y] else y,res)
        
    


if __name__ =='__main__': 
    cols = ['age','income','student','credit','buyComputer']
    data = pd.read_table('D:/$Python data analysis/DataMining/SSet.txt',sep=',',header=0,names=cols,engine = 'python')
    attrs = ['age','income','student','credit']
    cls = 'buyComputer'
    sample = {'age':'<=30','income':'middle','student':'T','credit':'middle'}
    print 'Buy computer?',bayes(data,attrs,cls,sample)
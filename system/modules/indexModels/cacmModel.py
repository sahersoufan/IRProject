import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import  cosine_similarity
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import FeatureUnion, Pipeline


########################################################################

transformer = None
tfidfTable  = None
def initializeTfidfTable(data: pd.DataFrame):
    ''' put cacm data in pipelinethen fit and transform it and return tfidf Table'''
    global transformer, tfidfTable
    transformer = FeatureUnion([
                      ('title_tfidf', 
                      Pipeline([
                        ('extract_field',
                                  FunctionTransformer(lambda x: x['.T'], 
                                                      validate=False)),
                                ('tfidf', 
                                  TfidfVectorizer(norm='l2' ,ngram_range=(1,2)))]))                              
                      ,('abstract_tfidf',
                     Pipeline([('extract_field',
                                FunctionTransformer(lambda x: x['.W'],
                                                      validate=False)),
                                ('tfidf',
                                  TfidfVectorizer(norm='l1',ngram_range=(1,2)))]))
                    ,('author_tfidf', 
                      Pipeline([('extract_field', 
                                  FunctionTransformer(lambda x: x['.A'], 
                                                      validate=False)),
                                ('tfidf', 
                                  TfidfVectorizer(norm='l1'))]))
    ])
    tfidfTable = transformer.fit_transform(data)

########################################################################

def getSimilars(query,n:int):
    ''' get the most n similar documents'''
    global transformer, tfidfTable
    querytfidf = transformer.transform(query)

    cos = cosine_similarity(querytfidf,tfidfTable).flatten()
    resultList = cos.argsort(axis=0)[-n:][::-1]
    return resultList

########################################################################

def queryingData(qDataFrame:pd.DataFrame,data:pd.DataFrame, n):
    ''' search for all queries in the queries file and get the most n similar document .I'''
    result = pd.DataFrame()
    for i in qDataFrame.index:
        try:
            resultDict:dict = {}
            tempIds:list = getSimilars(pd.DataFrame(qDataFrame.loc[qDataFrame.index == i,:]), n)

            tempList = []
            for id in tempIds:
                tempList.append(data.loc[id,'.I'])

            for id in range(1,n+1):
                resultDict[str(id)] = tempList[id - 1]
            result = result.append(resultDict, ignore_index=True)
        except:
            print(i)
            raise
    return result

########################################################################

def search(qDF:pd.DataFrame,data:pd.DataFrame, n):
    ''' search for input and return list of ids of the result'''
    try:
        resultlis = []
        tempIds = getSimilars(qDF, n)
        tempList = []
        for id in tempIds:
            tempList.append(data.loc[id,'.I'])

        for id in range(0,n):
            resultlis.append(tempList[id])
        return resultlis
    except:
        raise

########################################################################

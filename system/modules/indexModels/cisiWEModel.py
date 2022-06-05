from email import contentmanager
import spacy
import pandas as pd
import numpy as np

NLP = spacy.load("en_core_web_md")
contentTable = None

########################################################################

def initializeWEModel(data: pd.DataFrame):
    '''initialize content model with data vectors''' 
    global contentTable
    contentTable =  [NLP(data.loc[i, 'data']) for i in data.index]

########################################################################

def getSimilars(query, n:int):
    ''' get the most n similar documents'''
    global contentTable, NLP
    qvector = NLP(query)
    similarities = []
    for i in contentTable:
        sim = qvector.similarity(i)
        similarities.append(sim)

    temp = np.array(similarities)
    return  temp.argsort(axis=0)[-n:][::-1]

########################################################################

def queryingData(qDataFrame:pd.DataFrame, data:pd.DataFrame, n):
    ''' search for all queries in the queries file and get the most n similar document .I'''
    
    result = pd.DataFrame()
    resultDict:dict = {}
    resultDictCopy = resultDict.copy()

    for i in qDataFrame.index:
       try:
            nearest = getSimilars(qDataFrame.loc[i,'data'], n)
            ids = []
            for i in nearest:
                ids.append(data.loc[i,'.I'])

            for id in range(1,n+1):
               resultDictCopy[str(id)] = ids[id - 1]

            result = result.append(resultDictCopy, ignore_index=True)
            resultDictCopy = resultDict.copy()
       except:
           print(i)
           raise

    return result   
    
########################################################################

def search(qDF:pd.DataFrame,data:pd.DataFrame, n):
    ''' search for input and return list of ids of the result'''
    try:
        resultlis = []
        tempIds = getSimilars(qDF.loc[0, 'data'], n)
        
        tempList = []
        for id in tempIds:
            tempList.append(data.loc[id,'.I'])

        for id in range(0,n):
            resultlis.append(tempList[id])
        return resultlis
    except:
        raise
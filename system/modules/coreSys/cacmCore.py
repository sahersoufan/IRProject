from ..distributers import cacmdistributer
from ..paths import paths 
from ..preprocessores import cacmPreProcess,cacmPreProcessWE, preprocessores
from ..indexModels import cacmModel,cacmWEModel
from ..evaluation import evaluation
import os.path
import pandas as pd
################################################################
#                              DATA
################################################################
#                           INITIALIZE
################################################################

cacmAfterPreprocessed = None
cacmAfterDistribute = None
def initializeCacmModel():
    global cacmAfterPreprocessed, cacmAfterDistribute
    cacmPureData = cacmdistributer.getData(paths.CACMDATA, cacmdistributer.ALLMARKERS)
    cacmAfterDistribute = cacmdistributer.distributeCacmData(cacmPureData)
    cacmAfterDistribute.fillna('', inplace=True)
    
    cacmAfterPreprocessed = cacmPreProcess.preprocessedCacmData(cacmAfterDistribute)
    cacmAfterPreprocessed.fillna('', inplace=True)

    cacmAfterDistribute.to_csv(paths.CACMCLEANEDDATA)
    cacmAfterPreprocessed.to_csv(paths.CACMPREPROCESSEDDATA)

    cacmModel.initializeTfidfTable(data=cacmAfterPreprocessed)
    

################################################################
#                           INITIALIZE WORD EMBEDDING
################################################################
cacmAfterPreprocessedWE = None

def initializeCacmWEModel():
    global cacmAfterPreprocessedWE
    cacmAfterPreprocessedWE = cacmPreProcessWE.preprocessedData(cacmAfterDistribute)
    cacmAfterPreprocessedWE.fillna('', inplace=True)

    cacmAfterPreprocessedWE.to_csv(paths.CACMPREPROCESSEDDATAWE)

    cacmWEModel.initializeWEModel(cacmAfterPreprocessedWE)


################################################################
#                           UP SERVER
################################################################

def upServer():
    if os.path.exists(path=paths.CACMPREPROCESSEDDATA) and \
        os.path.exists(path=paths.CACMCLEANEDDATA):
        global cacmAfterPreprocessed, cacmAfterDistribute
        cacmAfterDistribute = pd.read_csv(paths.CACMCLEANEDDATA)
        cacmAfterDistribute.fillna('', inplace=True)

        cacmAfterPreprocessed = pd.read_csv(paths.CACMPREPROCESSEDDATA)
        cacmAfterPreprocessed.fillna('', inplace=True)

        cacmModel.initializeTfidfTable(data=cacmAfterPreprocessed)
    else:
        initializeCacmModel()

################################################################

def upServerWE():
    if os.path.exists(path=paths.CACMPREPROCESSEDDATAWE):
        global cacmAfterPreprocessedWE
        cacmAfterPreprocessedWE = pd.read_csv(paths.CACMPREPROCESSEDDATAWE)
        cacmAfterPreprocessedWE.fillna('', inplace=True)

        cacmWEModel.initializeWEModel(cacmAfterPreprocessedWE)
    else:
        initializeCacmWEModel()

################################################################
#                              QUERY
################################################################
#                           INITIALIZE
################################################################

cacmQuAfPre = None

def initializeCacmQuery():
    cacmPureQuery = cacmdistributer.getData(paths.CACMQUERY ,cacmdistributer.QUERYMARKERS)
    cacmAfDist = cacmdistributer.distributeCacmQueries(cacmPureQuery)
    cacmAfDist.fillna('', inplace=True)
    global cacmQuAfPre
    cacmQuAfPre = cacmPreProcess.preprocesseQuery(cacmAfDist)
    cacmQuAfPre.fillna('', inplace=True)
    cacmQuAfPre.to_csv(paths.CACMPREPROCESSEDQUERY)

################################################################
#                           INITIALIZE WORD EMBEDDING
################################################################
cacmWEQuAfPre = None
def initializeCacmWEQuery():
    cacmPureQuery = cacmdistributer.getData(paths.CACMQUERY ,cacmdistributer.QUERYMARKERS)
    cacmAfDist = cacmdistributer.distributeCacmQueries(cacmPureQuery)
    cacmAfDist.fillna('', inplace=True)

    global cacmWEQuAfPre
    cacmQuAfPre = cacmPreProcessWE.preprocesseQuery(cacmAfDist)
    cacmQuAfPre.fillna('', inplace=True)

    cacmQuAfPre.to_csv(paths.CACMPREPROCESSEDQUERYWE)

################################################################
#                           UP SERVER
################################################################

def upServerQuery():
    if os.path.exists(path=paths.CACMPREPROCESSEDQUERY):
        global cacmQuAfPre
        cacmQuAfPre = pd.read_csv(paths.CACMPREPROCESSEDQUERY)
        cacmQuAfPre.fillna('', inplace=True)
    else:
        initializeCacmQuery()

################################################################

def upServerWEQuery():
    if os.path.exists(path=paths.CACMPREPROCESSEDQUERYWE):
        global cacmWEQuAfPre
        cacmWEQuAfPre = pd.read_csv(paths.CACMPREPROCESSEDQUERYWE)
        cacmWEQuAfPre.fillna('', inplace=True)
    else:
        initializeCacmWEQuery()

################################################################
#                              QRELS
################################################################
#                           INITIALIZE
################################################################

cacmQRELAfCl = None

def initializeCacmQREL():
    cacmPureQREL = cacmdistributer.getRles(paths.CACMQRELS)
    global cacmQRELAfCl
    cacmQRELAfCl = cacmdistributer.distributeCacmQrel(cacmPureQREL)
    cacmQRELAfCl.fillna('', inplace=True)
    cacmQRELAfCl.to_csv(paths.CACMCLEANEDQRELS)

################################################################
#                           INITIALIZE WORD EMBEDDING
################################################################



################################################################
#                           UP SERVER
################################################################

def upServerQREL():
    if os.path.exists(path=paths.CACMCLEANEDQRELS):
        global cacmQRELAfCl
        cacmQRELAfCl = pd.read_csv(paths.CACMCLEANEDQRELS)
        cacmQRELAfCl.fillna('', inplace=True)
    else:
        initializeCacmQREL()









################################################################
#                           EVALUATE 
################################################################

def evaluateSearch(n = 10):
    dataPD = cacmModel.queryingData(cacmQuAfPre, cacmAfterPreprocessed, n)
    precisionAtN = evaluation.calcPrecisionAtK(dataPD, cacmQRELAfCl)
    recallAtN = evaluation.calcRecallAtK(dataPD, cacmQRELAfCl)
    meanAveragePrecision = evaluation.calcMAPrecisionAtK(dataPD, cacmQRELAfCl)
    meanReciprocalRank = evaluation.calcMeanReciprocalRank(dataPD, cacmQRELAfCl)

    evaluateObj = {
        'result':{
            'precision':precisionAtN,
            'recall':recallAtN,
            'MAP': meanAveragePrecision,
            'MRR': meanReciprocalRank
        }
    }
    
    # print(f'precacmon@{n} : {precacmonAtN}')
    # print(f'recall@{n} : {recallAtN}')
    # print(f'MAP : {meanAveragePrecacmon}')
    # print(f'MRR : {meanRecimeanAveragePrecacmonprocalRank}')

    return evaluateObj

################################################################

def evaluateWESearch(n = 10):
    dataPD = cacmWEModel.queryingData(cacmWEQuAfPre, cacmAfterPreprocessed, n)

    precacmonAtN = evaluation.calcPrecisionAtK(dataPD, cacmQRELAfCl)
    recallAtN = evaluation.calcRecallAtK(dataPD, cacmQRELAfCl)
    meanAveragePrecision = evaluation.calcMAPrecisionAtK(dataPD, cacmQRELAfCl)
    meanReciprocalRank = evaluation.calcMeanReciprocalRank(dataPD, cacmQRELAfCl)

    evaluateObj = {
        'result':{
            'precacmon':precacmonAtN,
            'recall':recallAtN,
            'MAP': meanAveragePrecision,
            'MRR': meanReciprocalRank
        }
    }
    
    # print(f'precacmon@{n} : {precacmonAtN}')
    # print(f'recall@{n} : {recallAtN}')
    # print(f'MAP : {meanAveragePrecacmon}')
    # print(f'MRR : {meanRecimeanAveragePrecacmonprocalRank}')

    return evaluateObj

################################################################
#                           SEARCH 
################################################################

def search(data, n):
    dataAfCorrection = preprocessores.correctWords(data)
    dataPD: pd.DataFrame = cacmPreProcess.preprocesseSearchInput(data)
    global cacmAfterPreprocessed, cacmAfterDistribute
    resultIds = cacmModel.search(dataPD, cacmAfterPreprocessed, n)
    resultDict = {
        'reslutDictionary':{
            'result':{},
            'correction':dataAfCorrection
        }
    }
    for i in range(0,len(resultIds)):
        resultDict['reslutDictionary']['result'][i] = \
        cacmAfterDistribute.loc[cacmAfterDistribute['.I'] ==  resultIds[i]\
            , ['.T', '.A', '.W']].to_dict()
    return resultDict

################################################################

def structuredSearch(data, n):
    # dataAfCorrection = preprocessores.correctWords(data)
    dataPD: pd.DataFrame = cacmPreProcess.preprocesseStructuredSearchInput(data)
    global cacmAfterPreprocessed, cacmAfterDistribute
    resultIds = cacmModel.search(dataPD, cacmAfterPreprocessed, n)
    resultDict = {
        'reslutDictionary':{
            'result':{}
            # 'correction':dataAfCorrection
        }
    }
    for i in range(0,len(resultIds)):
        resultDict['reslutDictionary']['result'][i] = \
        cacmAfterDistribute.loc[cacmAfterDistribute['.I'] ==  resultIds[i]\
            , ['.T', '.A', '.W']].to_dict()
    return resultDict

################################################################

def searchWE(data, n):
    dataAfCorrection = preprocessores.correctWords(data)
    dataPD: pd.DataFrame = cacmPreProcessWE.preprocesseSearchInput(data)
    global cacmAfterPreprocessed, cacmAfterDistribute
    resultIds = cacmWEModel.search(dataPD, cacmAfterPreprocessed, n)
    resultDict = {
        'reslutDictionary':{
            'result':{},
            'correction':dataAfCorrection
        }
    }
    for i in range(0,len(resultIds)):
        resultDict['reslutDictionary']['result'][i] = \
        cacmAfterDistribute.loc[cacmAfterDistribute['.I'] ==  resultIds[i]\
            , ['.T', '.A', '.W']].to_dict()
    return resultDict

################################################################

def structuredSearchWE(data, n):
    # dataAfCorrection = preprocessores.correctWords(data)
    dataPD: pd.DataFrame = cacmPreProcessWE.preprocesseStructuredSearchInput(data)
    global cacmAfterPreprocessed, cacmAfterDistribute
    resultIds = cacmWEModel.search(dataPD, cacmAfterPreprocessed, n)
    resultDict = {
        'reslutDictionary':{
            'result':{}
            # 'correction':dataAfCorrection
        }
    }
    for i in range(0,len(resultIds)):
        resultDict['reslutDictionary']['result'][i] = \
        cacmAfterDistribute.loc[cacmAfterDistribute['.I'] ==  resultIds[i]\
            , ['.T', '.A', '.W']].to_dict()
    return resultDict
from unittest import skip
from ..distributers import cisidistibuter
from ..paths import paths 
from ..preprocessores import cisiPreProcess,cisiPreProcessWE, preprocessores
from ..indexModels import cisiModel,cisiWEModel
from ..evaluation import evaluation
import os.path
import pandas as pd
################################################################
#                              DATA
################################################################
#                           INITIALIZE
################################################################

cisiAfterPreprocessed = None
cisiAfterDistribute = None
def initializeCisimodel():
    global cisiAfterPreprocessed, cisiAfterDistribute
    cisiPureData = cisidistibuter.getData(paths.CISIDATA, cisidistibuter.ALLMARKERS)
    cisiAfterDistribute = cisidistibuter.distributeCisiData(cisiPureData)
    cisiAfterDistribute.fillna('', inplace=True)
    
    cisiAfterPreprocessed = cisiPreProcess.preprocessedCisiData(cisiAfterDistribute)
    cisiAfterPreprocessed.fillna('', inplace=True)
    cisiAfterPreprocessed['.B'] = pd.to_datetime(cisiAfterPreprocessed['.B'])

    cisiAfterDistribute.to_csv(paths.CISICLEANEDDATA)
    cisiAfterPreprocessed.to_csv(paths.CISIPREPROCESSEDDATA)

    cisiModel.initializeTfidfTable(data=cisiAfterPreprocessed)
    

################################################################
#                           INITIALIZE WORD EMBEDDING
################################################################
cisiAfterPreprocessedWE = None

def initializeCisiWEmodel():
    global cisiAfterPreprocessedWE
    cisiAfterPreprocessedWE = cisiPreProcessWE.preprocessedData(cisiAfterDistribute)
    cisiAfterPreprocessedWE.fillna('', inplace=True)
    cisiAfterPreprocessedWE.to_csv(paths.CISIPREPROCESSEDDATAWE)
    cisiAfterPreprocessedWE['.B'] = pd.to_datetime(cisiAfterPreprocessedWE['.B'])

    cisiWEModel.initializeWEModel(cisiAfterPreprocessedWE)


################################################################
#                           UP SERVER
################################################################

def upServer():
    if os.path.exists(path=paths.CISIPREPROCESSEDDATA) and \
        os.path.exists(path=paths.CISICLEANEDDATA):
        global cisiAfterPreprocessed, cisiAfterDistribute
        cisiAfterDistribute = pd.read_csv(paths.CISICLEANEDDATA)
        cisiAfterDistribute.fillna('', inplace=True)

        cisiAfterPreprocessed = pd.read_csv(paths.CISIPREPROCESSEDDATA)
        cisiAfterPreprocessed.fillna('', inplace=True)
        cisiAfterPreprocessed['.B'] = pd.to_datetime(cisiAfterPreprocessed['.B'])

        cisiModel.initializeTfidfTable(data=cisiAfterPreprocessed)
    else:
        initializeCisimodel()

################################################################

def upServerWE():
    if os.path.exists(path=paths.CISIPREPROCESSEDDATAWE):
        global cisiAfterPreprocessedWE, cisiAfterDistribute

        cisiAfterDistribute = pd.read_csv(paths.CISICLEANEDDATA)
        cisiAfterDistribute.fillna('', inplace=True)

        cisiAfterPreprocessedWE = pd.read_csv(paths.CISIPREPROCESSEDDATAWE)
        cisiAfterPreprocessedWE.fillna('', inplace=True)
        cisiAfterPreprocessedWE['.B'] = pd.to_datetime(cisiAfterPreprocessedWE['.B'])

        cisiWEModel.initializeWEModel(cisiAfterPreprocessedWE)
    else:
        initializeCisiWEmodel()

################################################################
#                              QUERY
################################################################
#                           INITIALIZE
################################################################

cisiQuAfPre = None

def initializeCisiQuery():
    cisiPureQuery = cisidistibuter.getData(paths.CISIQUERY ,cisidistibuter.QUERYMARKERS)
    cisiAfDist = cisidistibuter.distributeCisiQueries(cisiPureQuery)
    cisiAfDist.fillna('', inplace=True)
    global cisiQuAfPre
    cisiQuAfPre = cisiPreProcess.preprocesseQuery(cisiAfDist)
    cisiQuAfPre.fillna('', inplace=True)
    cisiQuAfPre.to_csv(paths.CISIPREPROCESSEDQUERY)

################################################################
#                           INITIALIZE WORD EMBEDDING
################################################################
cisiWEQuAfPre = None
def initializeCisiWEQuery():
    cisiPureQuery = cisidistibuter.getData(paths.CISIQUERY ,cisidistibuter.QUERYMARKERS)
    cisiAfDist = cisidistibuter.distributeCisiQueries(cisiPureQuery)
    cisiAfDist.fillna('', inplace=True)

    global cisiWEQuAfPre
    cisiQuAfPre = cisiPreProcessWE.preprocesseQuery(cisiAfDist)
    cisiQuAfPre.fillna('', inplace=True)

    cisiQuAfPre.to_csv(paths.CISIPREPROCESSEDQUERYWE)

################################################################
#                           UP SERVER
################################################################

def upServerQuery():
    if os.path.exists(path=paths.CISIPREPROCESSEDQUERY):
        global cisiQuAfPre
        cisiQuAfPre = pd.read_csv(paths.CISIPREPROCESSEDQUERY)
        cisiQuAfPre.fillna('', inplace=True)
    else:
        initializeCisiQuery()

################################################################

def upServerWEQuery():
    if os.path.exists(path=paths.CISIPREPROCESSEDQUERYWE):
        global cisiWEQuAfPre
        cisiWEQuAfPre = pd.read_csv(paths.CISIPREPROCESSEDQUERYWE)
        cisiWEQuAfPre.fillna('', inplace=True)
    else:
        initializeCisiWEQuery()

################################################################
#                              QRELS
################################################################
#                           INITIALIZE
################################################################

cisiQRELAfCl = None

def initializeCisiQREL():
    cisiPureQREL = cisidistibuter.getRles(paths.CISIQRELS)
    global cisiQRELAfCl
    cisiQRELAfCl = cisidistibuter.distributeCisiQrel(cisiPureQREL)
    cisiQRELAfCl.fillna('', inplace=True)
    cisiQRELAfCl.to_csv(paths.CISICLEANEDQRELS)

################################################################
#                           INITIALIZE WORD EMBEDDING
################################################################



################################################################
#                           UP SERVER
################################################################

def upServerQREL():
    if os.path.exists(path=paths.CISICLEANEDQRELS):
        global cisiQRELAfCl
        cisiQRELAfCl = pd.read_csv(paths.CISICLEANEDQRELS)
        cisiQRELAfCl.fillna('', inplace=True)
    else:
        initializeCisiQREL()









################################################################
#                           EVALUATE 
################################################################

def evaluateSearch(n = 10):
    dataPD = cisiModel.queryingData(cisiQuAfPre, cisiAfterPreprocessed, n)
    precisionAtN = evaluation.calcPrecisionAtK(dataPD, cisiQRELAfCl)
    recallAtN = evaluation.calcRecallAtK(dataPD, cisiQRELAfCl)
    meanAveragePrecision = evaluation.calcMAPrecisionAtK(dataPD, cisiQRELAfCl)
    meanRecimeanAveragePrecisionprocalRank = evaluation.calcMeanReciprocalRank(dataPD, cisiQRELAfCl)

    evaluateObj = {
        'result':{
            'precision':precisionAtN,
            'recall':recallAtN,
            'MAP': meanAveragePrecision,
            'MRR': meanRecimeanAveragePrecisionprocalRank
        }
    }
    
    # print(f'precision@{n} : {precisionAtN}')
    # print(f'recall@{n} : {recallAtN}')
    # print(f'MAP : {meanAveragePrecision}')
    # print(f'MRR : {meanRecimeanAveragePrecisionprocalRank}')

    return evaluateObj

################################################################

def evaluateWESearch(n = 10):
    dataPD = cisiWEModel.queryingData(cisiWEQuAfPre, cisiAfterPreprocessed, n)

    precisionAtN = evaluation.calcPrecisionAtK(dataPD, cisiQRELAfCl)
    recallAtN = evaluation.calcRecallAtK(dataPD, cisiQRELAfCl)
    meanAveragePrecision = evaluation.calcMAPrecisionAtK(dataPD, cisiQRELAfCl)
    meanRecimeanAveragePrecisionprocalRank = evaluation.calcMeanReciprocalRank(dataPD, cisiQRELAfCl)

    evaluateObj = {
        'result':{
            'precision':precisionAtN,
            'recall':recallAtN,
            'MAP': meanAveragePrecision,
            'MRR': meanRecimeanAveragePrecisionprocalRank
        }
    }
    
    # print(f'precision@{n} : {precisionAtN}')
    # print(f'recall@{n} : {recallAtN}')
    # print(f'MAP : {meanAveragePrecision}')
    # print(f'MRR : {meanRecimeanAveragePrecisionprocalRank}')

    return evaluateObj

################################################################
#                           SEARCH 
################################################################

def search(data):
    dataAfCorrection = preprocessores.correctWords(data.get('query'))
    dataPD: pd.DataFrame = cisiPreProcess.preprocesseSearchInput(data)
    global cisiAfterPreprocessed, cisiAfterDistribute
    resultIds = cisiModel.search(dataPD, cisiAfterPreprocessed, data.get('n'))
    resultDict = {
        'reslutDictionary':{
            'result':{},
            'correction':dataAfCorrection
        }
    }
    return resultToDict(resultDict, resultIds)


################################################################

def structuredSearch(data):
    # dataAfCorrection = preprocessores.correctWords(data)
    dataPD: pd.DataFrame = cisiPreProcess.preprocesseStructuredSearchInput(data)
    global cisiAfterPreprocessed, cisiAfterDistribute
    resultIds = cisiModel.search(dataPD, cisiAfterPreprocessed, data.get('n'))
    resultDict = {
        'reslutDictionary':{
            'result':{}
            # 'correction':dataAfCorrection
        }
    }

    return resultToDict(resultDict, resultIds)



################################################################

def searchWE(data):
    dataAfCorrection = preprocessores.correctWords(data.get('query'))
    dataPD: pd.DataFrame = cisiPreProcessWE.preprocesseSearchInput(data)
    global cisiAfterPreprocessedWE
    resultIds = cisiWEModel.search(dataPD, cisiAfterPreprocessedWE, data.get('n'))
    resultDict = {
        'reslutDictionary':{
            'result':{},
            'correction':dataAfCorrection
        }
    }
    return resultToDict(resultDict, resultIds)


################################################################

def structuredSearchWE(data):
    # dataAfCorrection = preprocessores.correctWords(data)
    dataPD: pd.DataFrame = cisiPreProcessWE.preprocesseStructuredSearchInput(data)
    global cisiAfterPreprocessedWE
    resultIds = cisiWEModel.search(dataPD, cisiAfterPreprocessedWE, data.get('n'))
    resultDict = {
        'reslutDictionary':{
            'result':{}
            # 'correction':dataAfCorrection
        }
    }
    return resultToDict(resultDict, resultIds)




################################################################
##                          HELPERS
################################################################
def resultToDict(resultDict, resultIds):
    global cisiAfterDistribute
    for i in range(0,len(resultIds)):
        temp = cisiAfterDistribute.loc[cisiAfterDistribute['.I'] == resultIds[i],\
             ['.T', '.A', '.W', '.B']].to_dict()
#TODO tell said about this
        tk = list(temp.keys())
        for sk in tk:
            k = list(temp[sk].keys())
            temp[sk] = temp[sk][k[0]]


        resultDict['reslutDictionary']['result'][i] = temp

    return resultDict
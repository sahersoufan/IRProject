from ..distributers import cisidistibuter
from ..paths import paths 
from ..preprocessores import cisiPreProcess
from ..indexModels import cisiModel
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

    cisiAfterPreprocessed.to_csv(paths.CISIPREPROCESSEDDATA)

    cisiModel.initializeTfidfTable(data=cisiAfterPreprocessed)
    
################################################################
#                           UP SERVER
################################################################

def upServer():
    if os.path.exists(path=paths.CISIPREPROCESSEDDATA):
        global cisiAfterPreprocessed
        cisiAfterPreprocessed = pd.read_csv(paths.CISIPREPROCESSEDDATA)
        cisiAfterPreprocessed.fillna('', inplace=True)
        cisiModel.initializeTfidfTable(data=cisiAfterPreprocessed)
    else:
        initializeCisimodel()

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
#                           INITIALIZE WORD EMBEDDING
################################################################







################################################################
#                           SEARCH 
################################################################

def evaluateSearch(n):
    dataPD = cisiModel.queryingData(cisiQuAfPre, cisiAfterPreprocessed, n)
    precisionAtN = evaluation.calc

################################################################

def search(data, n):
    dataPD: pd.DataFrame = cisiPreProcess.preprocesseSearchInput(data)
    global cisiAfterPreprocessed
    resultIds = cisiModel.search(dataPD, cisiAfterPreprocessed, n)
    resultDict = {}
    for i,j in resultIds, range(0,len(resultIds)):
        resultDict[j] = resultIds.loc[resultIds['.I'] == i, ['.T', '.A', '.W']].to_dict()
    
    return resultDict
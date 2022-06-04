import pandas as pd
from sklearn.metrics import precision_score, recall_score

def reSizeLists(l1:list, l2:list):
    '''resize lists to have the same len'''
    if len(l1) < len(l2):
        l2 = l2[0:len(l1)]
    while len(l1) > len(l2):
        l1 = l1[0:len(l2)]

    return l1, l2

########################################################################

def precWithoutOrder(l1:list,l2:list):
    ''' calculate precision witout orering'''
    try:
        return len(set(l1).intersection(set(l2))) / len(l2)
    except:
        return 0

########################################################################

def calcMAPrecisionAtK(resData:pd.DataFrame, qrelsData: pd.DataFrame):
    '''calcualte MAP (average precision on multiple queries)'''
    precisionsAtK:list = []
    precisionAtK:float

    for i in resData.index:
        precisionOnQuery = []
        resArray = resData.loc[i].to_numpy()
        qresArray = qrelsData.loc[qrelsData['.I'] == i+1, 'data'].to_numpy()
        
        if len(qresArray) == 0: 
            continue

        resArray, qresArray = reSizeLists(resArray, qresArray)

        for lenI in range(0,len(qresArray)):
            tempRes:list = resArray[0:lenI+1].tolist()
            tempQRes:list = qresArray[0:lenI+1].tolist()
            precisionOnQuery.append(precision_score(tempQRes, tempRes, average='micro'))
        
        try:
            precisionsAtK.append(sum(precisionOnQuery) / len(precisionOnQuery))
        except ZeroDivisionError: 
            precisionsAtK.append(0)

    precisionAtK = sum(precisionsAtK) / len(precisionsAtK)
    return precisionAtK



########################################################################

def calcAveragePrecisionAtK(resData:pd.DataFrame, qrelsData: pd.DataFrame):
    '''calcualte just Average Precision for one query or more'''
    precisionsAtK:list = []

    for i in resData.index:
        precisionOnQuery = []

        resArray = resData.loc[i].to_numpy()
        qresArray = qrelsData.loc[qrelsData['.I'] == i+1, 'data'].to_numpy()
        
        if len(qresArray) == 0: 
            continue

        resArray, qresArray = reSizeLists(resArray, qresArray)

        for lenI in range(0,len(qresArray)):

            tempRes:list = resArray[0:lenI+1].tolist()
            tempQRes:list = qresArray[0:lenI+1].tolist()
            precisionOnQuery.append(precision_score(tempQRes, tempRes, average='micro'))

        try:
            precisionsAtK.append(sum(precisionOnQuery) / len(precisionOnQuery))
        except ZeroDivisionError: 
            precisionsAtK.append(0)
    return precisionsAtK

########################################################################


def calcPrecisionAtK(resData:pd.DataFrame, qrelsData: pd.DataFrame):
    '''calcualte just Precision for one query or more'''
    precisionsAtK:list = []

    for i in resData.index:
        precisionOnQuery = []

        resArray = resData.loc[i].to_numpy()
        qresArray = qrelsData.loc[qrelsData['.I'] == i+1, 'data'].to_numpy()
        
        if len(qresArray) == 0: 
            continue

        resArray, qresArray = reSizeLists(resArray, qresArray)
        precisionsAtK.append(precision_score(qresArray, resArray, average='micro'))

    return precisionsAtK

########################################################################

















########################################################################

def calcMAPrecisionAtKOrder(resData:pd.DataFrame, qrelsData: pd.DataFrame):
    '''calcualte MAP (average precision on multiple queries) without order'''
    precisionsAtK:list = []
    precisionAtK:float

    for i in resData.index:
        resArray = resData.loc[i].to_numpy()
        qresArray = qrelsData.loc[qrelsData['.I'] == i+1, 'data'].to_numpy()
        
        if len(qresArray) == 0: 
            continue

        resArray, qresArray = reSizeLists(resArray, qresArray)

        prec = precWithoutOrder(qresArray, resArray)

        precisionsAtK.append(prec)

    precisionAtK = sum(precisionsAtK) / len(precisionsAtK)
    return precisionAtK



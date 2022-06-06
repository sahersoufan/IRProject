from .preprocessores import *
import pandas as pd

########################################################################
#                           data section
########################################################################

def TitlePreProcesse(t):
    '''do preprocess methods on titles'''
    tempText = toLower(t)
    tempText = removePunctuation(tempText)
    tempText = converteNumbers(tempText)
    tempText = removeWhiteSpace(tempText)
    tempText = removeStopWords(tempText)
    tempText = stemWords(tempText)
    tempText = lemmatizeWords(tempText)

    return tempText

########################################################################

def abstractPreProcesse(a):
    '''do preprocess methods on abstract'''
    tempText = toLower(a)
    tempText = removePunctuation(tempText)
    tempText = converteNumbers(tempText)
    tempText = removeWhiteSpace(tempText)
    tempText = removeStopWords(tempText)
    tempText = stemWords(tempText)
    tempText = lemmatizeWords(tempText)
    tempText = removeOutliers(tempText)

    return tempText

########################################################################

def authorPreProcesse(a):
    '''do preprocess methods on authors'''
    tempText = toLower(a)
    lis = tempText.split(' ')
    names = ' '
    l = []
    for word in lis:
      if ',' in word:
          l.append(removePunctuation(word))
    names = ' '.join(l)

    return names

########################################################################

def publicationPreProcesse(p): 
    try:
        return pd.to_datetime(p)
    except:
        return ''

########################################################################        

def preprocessedCisiData(dataFrame:pd.DataFrame):
    '''take pandas dataFrame with coulmns = {.I, .T, .A, .W} which contain Cisi data and preprocess it'''
    pdataFrame = pd.DataFrame()
    seriesDict:dict = {} 
    seriesData = seriesDict.copy()
    for i in dataFrame.index:
        try:
            tempT = tempA = tempW = tempB = None
            if not dataFrame.loc[i, '.T'] == '':
                tempT = TitlePreProcesse(dataFrame.loc[i, '.T'])
            if not dataFrame.loc[i, '.A'] == '':
                tempA = authorPreProcesse(dataFrame.loc[i, '.A'])
            if not dataFrame.loc[i, '.W'] == '':
                tempW = abstractPreProcesse(dataFrame.loc[i, '.W'])
            if not dataFrame.loc[i, '.B'] == '':
                tempB = publicationPreProcesse(dataFrame.loc[i, '.B'])            


            seriesData['.I'] = i+1
            seriesData['.T'] = tempT
            seriesData['.A'] = tempA
            seriesData['.W'] = tempW
            seriesData['.B'] = tempB
            
            pdataFrame = pdataFrame.append(seriesData, ignore_index=True)
        except:
            print(i)
            raise 
    
    pdataFrame.fillna('', inplace=True)
    return pdataFrame

########################################################################
#                           query section
########################################################################


def qTitlePreProcesse(t):
    '''do preprocess methods on query titles'''
    tempText = toLower(t)
    tempText = removePunctuation(tempText)
    tempText = converteNumbers(tempText)
    tempText = removeWhiteSpace(tempText)
    tempText = removeStopWords(tempText)
    tempText = stemWords(tempText)
    tempText = lemmatizeWords(tempText)

    return tempText

########################################################################

def qAbstractPreProcesse(a):
    '''do preprocess methods on query abstract'''
    tempText = toLower(a)
    tempText = removePunctuation(tempText)
    tempText = converteNumbers(tempText)
    tempText = removeWhiteSpace(tempText)
    tempText = removeStopWords(tempText)
    tempText = stemWords(tempText)
    tempText = lemmatizeWords(tempText)
    tempText = removeOutliers(tempText)
    return tempText

########################################################################

def qAuthorPreProcesse(a):
    '''do preprocess methods on query authors'''
    tempText = toLower(a)
    lis = tempText.split(' ')
    names = ' '
    l = []
    for word in lis:
      if ',' in word:
          l.append(removePunctuation(word))
    names = ' '.join(l)
    return names

########################################################################

def preprocesseQuery(dataFrame:pd.DataFrame):
    pdataFrame = pd.DataFrame() 
    seriesDict:dict = {} 
    seriesData = seriesDict.copy()
    for i in dataFrame.index:
        try:
            tempT = tempA = tempW  = None
            if not dataFrame.loc[i, '.T'] == '':
                tempT = qTitlePreProcesse(dataFrame.loc[i, '.T'])
            if not dataFrame.loc[i, '.A'] == '':
                tempA = qAuthorPreProcesse(dataFrame.loc[i, '.A'])
            if not dataFrame.loc[i, '.W'] == '':
                tempW = qAbstractPreProcesse(dataFrame.loc[i, '.W'])
                if dataFrame.loc[i, '.T'] == '':
                    tempT = addMostFreq(tempW)
                    

                
            seriesData['.I'] = i+1
            seriesData['.T'] = tempT
            seriesData['.A'] = tempA
            seriesData['.W'] = tempW
            pdataFrame = pdataFrame.append(seriesData, ignore_index=True)
        except:
            print(i)
            raise 
    
    pdataFrame.fillna('', inplace=True)
    return pdataFrame


########################################################################
#                           search input section
########################################################################

def preprocesseSearchInput(dataDic) -> pd.DataFrame:
    psi = pd.DataFrame()
    seriesDict:dict = {} 

    data = dataDic.get('query')

    tempI = 1
    tempW = qAbstractPreProcesse(data)
    tempT = addMostFreq(tempW)
    tempA = ''
    try:
        tempB = pd.to_datetime(dataDic.get('date'))
    except:
        tempB = ''

    seriesDict['.I'] = tempI
    seriesDict['.T'] = tempT
    seriesDict['.A'] = tempA
    seriesDict['.W'] = tempW
    seriesDict['.B'] = tempB
   
    psi = psi.append(seriesDict, ignore_index=True)
    psi.fillna('', inplace=True)

    return psi

########################################################################

def SEAuthorPreProcesse(a):
    tempText = a
    tempText = toLower(tempText)
    lis = tempText.split(' ')
    names = ' '
    l = []
    for word in lis:
          l.append(removePunctuation(word))
    names = ' '.join(l)
    return names

########################################################################

def preprocesseStructuredSearchInput(dataDic) -> pd.DataFrame:
    psi = pd.DataFrame()
    seriesDict:dict = {} 

    data = dataDic.get('query')

    tempI = 1
    tempW = qAbstractPreProcesse(data.get('.W'))
    tempT = qTitlePreProcesse(data.get('.T'))
    tempA = SEAuthorPreProcesse(data.get('.A'))
    try:
        tempB = pd.to_datetime(dataDic.get('date'))
    except:
        tempB = ''

    seriesDict['.I'] = tempI
    seriesDict['.T'] = tempT
    seriesDict['.A'] = tempA
    seriesDict['.W'] = tempW
    seriesDict['.B'] = tempB

    psi = psi.append(seriesDict, ignore_index=True)
    psi.fillna('', inplace=True)

    return psi





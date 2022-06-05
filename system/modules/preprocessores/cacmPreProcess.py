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
    tempText = p.replace('CACM ','')
    return pd.to_datetime(tempText)

########################################################################

def preprocessedCacmData(dataFrame:pd.DataFrame):
    '''take pandas dataFrame with coulmns = {.I, .T, .A, .W, .B} which contain Cacm data and preprocess it'''
    pdataFrame = pd.DataFrame()
    seriesDict:dict = {} 
    seriesData = seriesDict.copy()
    for i in dataFrame.index:
        try:
            tempT = tempA = tempW  = None
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

def preprocesseSearchInput(data) -> pd.DataFrame:
    psi = pd.DataFrame()
    seriesDict:dict = {} 

    tempI = 1
    tempW = qAbstractPreProcesse(data)
    tempT = addMostFreq(tempW)
    tempA = ''

    seriesDict['.I'] = tempI
    seriesDict['.T'] = tempT
    seriesDict['.A'] = tempA
    seriesDict['.W'] = tempW

    psi = psi.append(seriesDict, ignore_index=True)
    psi.fillna('', inplace=True)

    return psi

########################################################################

def preprocesseStructuredSearchInput(data) -> pd.DataFrame:
    psi = pd.DataFrame()
    seriesDict:dict = {} 

    tempI = 1
    tempW = qAbstractPreProcesse(data.get('.W'))
    tempT = qTitlePreProcesse(data.get('.T'))
    tempA = qAuthorPreProcesse(data.get('.A'))

    seriesDict['.I'] = tempI
    seriesDict['.T'] = tempT
    seriesDict['.A'] = tempA
    seriesDict['.W'] = tempW

    psi = psi.append(seriesDict, ignore_index=True)
    psi.fillna('', inplace=True)

    return psi





from .preprocessores import *
import pandas as pd

########################################################################
#                           data section
########################################################################


def TitlePreProcesse(t):
    '''do preprocess methods on titles'''

    tempText = t
    tempText = toLower(t)
    tempText = removePunctuation(tempText)
    tempText = removeWhiteSpace(tempText)
    return tempText

########################################################################

def abstractPreProcesse(a):
    '''do preprocess methods on abstract'''

    tempText = a
    tempText = toLower(a)
    tempText = removePunctuation(tempText)
    tempText = removeWhiteSpace(tempText)

    return tempText

########################################################################

def authorPreProcesse(a):
    '''do preprocess methods on authors'''

    tempText = a
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
        return None

########################################################################

def preprocessedData(dataFrame:pd.DataFrame):
    pdataFrame = pd.DataFrame()
    seriesDict:dict = {} 
    for i in dataFrame.index:
        try:
            tempT = tempA = tempW = ''
            tempB = None
            if not dataFrame.loc[i, '.T'] == '':
                tempT = TitlePreProcesse(dataFrame.loc[i, '.T'])
            if not dataFrame.loc[i, '.A'] == '':
                tempA = authorPreProcesse(dataFrame.loc[i, '.A'])
            if not dataFrame.loc[i, '.B'] == '':
                tempB = publicationPreProcesse(dataFrame.loc[i, '.B'])

            if not dataFrame.loc[i, '.W'] == '':
                tempW = abstractPreProcesse(dataFrame.loc[i, '.W'])
                    

            seriesDict['.I'] = i+1
            seriesDict['data'] = ' '.join([tempT, tempA, tempW])
            seriesDict['.B'] = tempB
            
            pdataFrame = pdataFrame.append(seriesDict, ignore_index=True)
            seriesDict = {}
        except:
            print(i)
            raise 
    pdataFrame.fillna('', inplace=True)
    return pdataFrame

########################################################################
#                           query section
########################################################################

import pandas as pd
import re


def qTitlePreProcesse(t):
    tempText = t
    tempText = toLower(tempText)
    tempText = removePunctuation(tempText)
    tempText = removeWhiteSpace(tempText)
    return tempText

########################################################################

def qAbstractPreProcesse(a):
    tempText = a
    tempText = toLower(tempText)
    tempText = removePunctuation(tempText)
    tempText = removeWhiteSpace(tempText)
    return tempText

########################################################################

def qAuthorPreProcesse(a):
    tempText = a
    tempText = toLower(tempText)
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
    qdataFrame = pd.DataFrame()
    seriesDict:dict = {} 
    for i in dataFrame.index:
        try:
            tempT = tempA = tempW = ''
            if not dataFrame.loc[i, '.T'] == '':
                tempT = TitlePreProcesse(dataFrame.loc[i, '.T'])
            if not dataFrame.loc[i, '.A'] == '':
                tempA = authorPreProcesse(dataFrame.loc[i, '.A'])
            if not dataFrame.loc[i, '.W'] == '':
                tempW = abstractPreProcesse(dataFrame.loc[i, '.W'])

            seriesDict['.I'] = i
            seriesDict['data'] = ' '.join([tempT, tempA, tempW])
            
            qdataFrame = qdataFrame.append(seriesDict, ignore_index=True)
            seriesDict = {}
        except:
            print(i)
            raise 
    qdataFrame.fillna('', inplace=True)
    return qdataFrame


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
    seriesDict['data'] = ' '.join([tempT, tempA, tempW])


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
    seriesDict['data'] = ' '.join([tempT, tempA, tempW])

    psi = psi.append(seriesDict, ignore_index=True)
    psi.fillna('', inplace=True)

    return psi


from dataclasses import dataclass
import pandas as pd
import re

IDMARKER = re.compile('(\.I.)')
ALLMARKERS = re.compile('(\.[ITWBACKNX] )')
QUERYMARKERS = re.compile('(\.[IWAN] )')

def getData(PATH, marker):
    """get the data from the file and split it by ID"""
    with open(PATH, 'r') as f:
        t = f.read().replace('\n', ' ')
        lines = re.split(marker, t)
        lines.pop(0)
    return lines

################################################################

def distributeCacmData(cacmData):
    ''' after doing getdata method on cacm.all this method converte it to dataframe'''
    dataFrame = pd.DataFrame(columns=['.I','.T','.W','.B','.A','.K','.C','.N','.X'])
    seriesDict:dict = {
        '.I': None,
        '.T': None,
        '.W': None,
        '.B': None,
        '.K': None,
        '.C': None,
        '.A': None,
        '.N': None,
        '.X': None
    }
    seriesData = seriesDict.copy()
    notTheFirst = False
    for i in range(0, len(cacmData), 2):
        if (notTheFirst and cacmData[i].strip() == '.I'):
            dataFrame = dataFrame.append(seriesData, ignore_index=True)
            seriesData = seriesDict.copy()

        seriesData[cacmData[i].strip()] = cacmData[i+1].strip()
        notTheFirst = True
    dataFrame = dataFrame.append(seriesData, ignore_index=True)
    return dataFrame
################################################################
#                           query section
################################################################

def distributeCacmQueries(cacmQuery):
    ''' after doing getdata method on cacm.qry this method converte it to dataframe'''
    qDataFrame = pd.DataFrame(columns=['.I','.T','.W','.A','.N'])
    seriesDict:dict = {
        '.I': None,
        '.T': None,
        '.W': None,
        '.A': None,
        '.N': None
    }
    seriesData = seriesDict.copy()
    notTheFirst = False
    for i in range(0, len(cacmQuery), 2):
        if (notTheFirst and cacmQuery[i].strip() == '.I'):
            qDataFrame = qDataFrame.append(seriesData, ignore_index=True)
            seriesData = seriesDict.copy()

        seriesData[cacmQuery[i].strip()] = cacmQuery[i+1].strip()
        notTheFirst = True
    qDataFrame = qDataFrame.append(seriesData, ignore_index=True)
    return qDataFrame
################################################################
#                           qrel section
################################################################


def getRles(path):
    with open(path, 'r') as f:
        global qrlesList
        qrlesList = f.read().split('\n')
        return qrlesList

################################################################

def distributeCacmQrel(qrelsData):

    qrelsFrame = pd.DataFrame(columns=['.I', 'data'])
    seriesDict:dict = {'.I':None, 'data':None}
    seriesData = seriesDict.copy()
    for i in qrelsData:
        try:
            #TODO may cause error
            element = i.split()
            seriesData['.I'] = int(element[0])
            seriesData['data'] = int(element[1])
            qrelsFrame = qrelsFrame.append(seriesData, ignore_index=True)
        except:
            pass
    return qrelsFrame

################################################################
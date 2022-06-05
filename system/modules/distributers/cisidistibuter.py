from dataclasses import dataclass
import pandas as pd
import re

IDMARKER = re.compile('(\.I.)')
ALLMARKERS = re.compile('(\.[ITABWX] )')
QUERYMARKERS = re.compile('(\.[ITAWB] )')

def getData(PATH, marker):
    """get the data from the file and split it by ID"""
    with open(PATH, 'r') as f:
        t = f.read().replace('\n', ' ')
        lines = re.split(marker, t)
        lines.pop(0)
    return lines

################################################################

def distributeCisiData(cisiData):
    ''' after doing getdata method on cisi.all this method converte it to dataframe'''
    dataFrame = pd.DataFrame(columns=['.I','.T','.A','.B','.W','.X'])
    seriesDict:dict = {
        '.I': None,
        '.T': None,
        '.A': None,
        '.B': None,
        '.W': None,
        '.X': None
    }
    seriesData = seriesDict.copy()
    notTheFirst = False
    for i in range(0, len(cisiData), 2):
        if (notTheFirst and cisiData[i].strip() == '.I'):
            dataFrame = dataFrame.append(seriesData, ignore_index=True)
            seriesData = seriesDict.copy()
        
        seriesData[cisiData[i].strip()] = cisiData[i+1].strip()
        notTheFirst = True
    dataFrame = dataFrame.append(seriesData, ignore_index=True)
    return dataFrame

################################################################
#                           query section
################################################################

def distributeCisiQueries(cisiQuery):
    ''' after doing getdata method on cisi.qry this method converte it to dataframe'''
    qDataFrame = pd.DataFrame(columns=['.I','.T','.A','.W','.B'])
    seriesDict:dict = {
        '.I': None,
        '.T': None,
        '.A': None,
        '.W': None,
        '.B': None
    }
    seriesData = seriesDict.copy()
    notTheFirst = False
    for i in range(0, len(cisiQuery), 2):
        if (notTheFirst and cisiQuery[i].strip() == '.I'):
            qDataFrame = qDataFrame.append(seriesData, ignore_index=True)
            seriesData = seriesDict.copy()

        seriesData[cisiQuery[i].strip()] = cisiQuery[i+1].strip()
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

def distributeCisiQrel(qrelsData):

    qrelsFrame = pd.DataFrame(columns=['.I', 'data'])
    seriesDict:dict = {'.I':None, 'data':None}
    seriesData = seriesDict.copy()
    for i in qrelsData:
        try:
            element = i.split()
            seriesData['.I'] = int(element[0])
            seriesData['data'] = int(element[1])
            qrelsFrame = qrelsFrame.append(seriesData, ignore_index=True)
        except:
            pass
    return qrelsFrame

################################################################
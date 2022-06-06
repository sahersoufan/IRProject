from .import cisiCore, cacmCore

corpus = 'corpus'
################################################################
#                           INITIALIZE 
################################################################
def initialize():
    #CISI
    cisiCore.initializeCisimodel()
    cisiCore.initializeCisiQuery()
    cisiCore.initializeCisiQREL()

    cisiCore.initializeCisiWEmodel()
    cisiCore.initializeCisiWEQuery()

    # #CACM
    cacmCore.initializeCacmModel()
    cacmCore.initializeCacmQuery()
    cacmCore.initializeCacmQREL()

    cacmCore.initializeCacmWEModel()
    cacmCore.initializeCacmWEQuery()


################################################################
#                           UP SERVER 
################################################################

def upServer():
    #CISI
    cisiCore.upServer()
    cisiCore.upServerQuery()
    cisiCore.upServerQREL()

    cisiCore.upServerWE()
    cisiCore.upServerWEQuery()

    #CACM
    cacmCore.upServer()
    cacmCore.upServerQuery()
    cacmCore.upServerQREL()

    cacmCore.upServerWE()
    cacmCore.upServerWEQuery()

################################################################
#                           SEARCH 
################################################################

def search(data:dict):
    if data.get(corpus) == 'cisi':
        if data.get('WE') == True:
            return cisiCore.searchWE(data)
        else:
            return cisiCore.search(data)

    elif data.get(corpus) == 'cacm':
        if data.get('WE') == True:
            return cacmCore.searchWE(data)
        else:
            return cacmCore.search(data)
    else:
        raise
################################################################

def structuredSearch(data:dict):
    if data.get(corpus) == 'cisi':
        if data.get('WE') == True:
            return cisiCore.structuredSearchWE(data)
        else:
            return cisiCore.structuredSearch(data)
    
    elif data.get(corpus) == 'cacm':
        if data.get('WE') == True:
            return cacmCore.structuredSearchWE(data)
        else:
            return cacmCore.structuredSearch(data)

    else:
        raise

################################################################

def evaluation(data):
    if data.get(corpus) == 'cisi':
        if data.get('WE') == True:
            return cisiCore.evaluateWESearch(data.get('n'))
        else:
            return cisiCore.evaluateSearch(data.get('n'))
    
    elif data.get(corpus) == 'cacm':
        if data.get('WE') == True:
            return cacmCore.evaluateWESearch(data.get('n'))
        else:
            return cacmCore.evaluateSearch(data.get('n'))
    else:
        raise    








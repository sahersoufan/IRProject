import cisiCore


################################################################
#                           INITIALIZE 
################################################################
def initialize(data:dict):
    if data.get('corpus') == 'cisi':
        cisiCore.initializeCisimodel()
        cisiCore.initializeCisiQuery()
        cisiCore.initializeCisiQREL()
    else:
        raise


################################################################
#                           UP SERVER 
################################################################

def upServer(data:dict):
    if data.get('corpus') == 'cisi':
        cisiCore.upServer()
        cisiCore.upServerQuery()
        cisiCore.upServerQREL()
    else:
        raise

################################################################
#                           SEARCH 
################################################################

def search(data:dict):

    if data.get('corpus') == 'cisi':
        return cisiCore.search(data=data.get('data', n=data.get('n')))
    else:
        raise


def evaluation(data:dict):
    if data.get('corpus') == 'cisi':
        return cisiCore.evaluateSearch(n=data.get('n'))
    else:
        raise    




################################################################
#                           INITIALIZE WORD EMBEDDING 
################################################################



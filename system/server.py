from flask import Flask, request, jsonify
from importlib_metadata import method_cache
from modules.coreSys import coreSys
port = 8000
app = Flask(__name__)


@app.route('/initialize', methods=['GET'])
def initialize():
    print("initialize")
    try:
        coreSys.initialize()
        return jsonify(success=True)
    except:
        return jsonify(success=False)


@app.route('/upserver', methods=['GET'])
def upserver():
    print('upserver')
    try:
        coreSys.upServer()
        return jsonify(success=True)
    except:
        return jsonify(success=False)   


@app.route('/evaluate', methods=['GET'])
def evaluateCisi():
    print('evaluate')
    try:
        data = request.get_json(force=True)
        res = coreSys.evaluation(data)
        return jsonify(res)
    except:
        return jsonify(success=False)   


@app.route('/search', methods=['GET'])
def search():
    print('search')
    try:
        data = request.get_json(force=True)
        res = coreSys.search(data)
        return jsonify(res)  
    except:
        raise #TODO handle
        return jsonify(success=False)

@app.route('/structuredSearch', methods=['GET'])
def structuredSearch():
    try:
        data = request.get_json(force=True)
        res = coreSys.structuredSearch(data)
        return jsonify(res)
    except:
        return jsonify(success=False)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)

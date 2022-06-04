from flask import Flask, request, jsonify

port = 8000
app = Flask(__name__)









if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)


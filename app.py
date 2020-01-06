from get_predictions import predict as pr
from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello! Send a request to /predict/:USERNAME to get results!'


@app.route('/predict/<username>/', methods=['GET'])
def predict(username):
    return jsonify(pr(username))


if __name__ == '__main__':
    app.run(threaded=True, port=5000)

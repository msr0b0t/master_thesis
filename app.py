from get_predictions import predict as pr
from flask import Flask, jsonify, request
from flask_cors import CORS
# from pymongo import MongoClient
# from bson import ObjectId

app = Flask(__name__)
cors = CORS(app)
# client = MongoClient()
# db = client["feedback-db"]

@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello! Send a request to /predict/:USERNAME to get results!'


@app.route('/predict/<username>/', methods=['GET'])
def predict(username):
    return jsonify(pr(username))


# @app.route('/feedback', methods=['POST'])
# def feedback():
#     data = request.get_json(force=True)
#     db.feedback.insert_one({
#         "user_selection": data["user_selection"],
#         "analysis_id": ObjectId(data["analysis_id"]),
#         "reasons": {reason.replace(".", ""): value for [reason, value] in data["reasons"]}
#     })
#     return jsonify({"ok": True})


if __name__ == '__main__':
    app.run(threaded=True, port=5000)

import os
from get_predictions import predict as pr
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
cors = CORS(app)
client = MongoClient(host=os.getenv("DB_HOST"), port=int(os.getenv("DB_PORT")), username=os.getenv(
	"DB_USERNAME"), password=os.getenv("DB_PASSWORD"), authSource=os.getenv("DB_AUTH_DB"))
db = client["locationuk"]


@app.route('/', methods=['GET'])
def hello_world():
	return 'Hello! Send a request to /predict/:USERNAME to get results!'


@app.route('/predict/<username>/', methods=['GET'])
def predict(username):
	return jsonify(pr(username))


@app.route('/feedback', methods=['POST'])
def feedback():
	data = request.get_json(force=True)
	db.bot_feedback.insert_one({
		"user_selection": data["user_selection"],
		"analysis_id": ObjectId(data["analysis_id"]),
		"reasons": {reason.replace(".", ""): value for [reason, value] in data["reasons"]}
	})
	return jsonify({"ok": True})


if __name__ == '__main__':
	app.run(threaded=True, port=5000)

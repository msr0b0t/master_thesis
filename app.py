import os
from get_predictions import predict as pr
from get_details import get_details as gd
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
from requests_oauthlib import OAuth1Session

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
	oauth_token = request.args.get('oauth_token')
	oauth_token_secret = request.args.get('oauth_token_secret')
	return jsonify(pr(username, oauth_token, oauth_token_secret))


@app.route('/details/<username>/', methods=['GET'])
def get_details(username):
	oauth_token = request.args.get('oauth_token')
	oauth_token_secret = request.args.get('oauth_token_secret')
	return jsonify(gd(username, oauth_token, oauth_token_secret))


@app.route('/feedback', methods=['POST'])
def feedback():
	data = request.get_json(force=True)
	db.bot_feedback.insert_one({
		"user_selection": data.get("user_selection", "-"),
		"analysis_id": ObjectId(data["analysis_id"]),
		"reasons": {reason.replace(".", ""): value for [reason, value] in data["reasons"]},
		"likert": int(data.get("likert", 0)),
		"suggestions": data.get("suggestions", "")
	})
	return jsonify({"ok": True})

@app.route("/req4req", methods=["GET"])
def req4req():
	request_token = OAuth1Session(client_key=os.getenv("OAUTH_TOKEN"), client_secret=os.getenv("OAUTH_TOKEN_SECRET"))
	data = request_token.get('https://api.twitter.com/oauth/request_token')
	oauth_token = str.split(str.split(data.text, '&')[0], '=')[1]
	oauth_token_secret = str.split(str.split(data.text, '&')[1], '=')[1]
	return {"ok": True, "oauth_token": oauth_token, "oauth_token_secret": oauth_token_secret}


@app.route("/req2acc", methods=["POST"])
def req2acc():
	payload = request.get_json(force=True)
	oauth_token = OAuth1Session(client_key=os.getenv("OAUTH_TOKEN"), client_secret=os.getenv("OAUTH_TOKEN_SECRET"),
                                resource_owner_key=payload["oauth_token"],
                                resource_owner_secret=payload["oauth_token_secret"])
	data = oauth_token.post('https://api.twitter.com/oauth/access_token', data={"oauth_verifier": payload["oauth_verifier"]})
	oauth_token = str.split(str.split(data.text, '&')[0], '=')[1]
	oauth_token_secret = str.split(str.split(data.text, '&')[1], '=')[1]
	user_id = str.split(str.split(data.text, '&')[2], '=')[1]
	screen_name = str.split(str.split(data.text, '&')[3], '=')[1]
	return {
		"ok": True,
		"oauth_token": oauth_token,
		"oauth_token_secret": oauth_token_secret,
		"user_id": user_id,
		"screen_name": screen_name
		}

if __name__ == '__main__':
	app.run(threaded=True, port=5000)

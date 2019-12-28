import pandas as pd
from pymongo import MongoClient


client = MongoClient()
users_collection = client["thesis-db"].users


data = []

for user in users_collection.find():
	user_vector = {
		"author_id": user["id_str"] if ("id_str" in user) else user["user"]["id_str"],
		"score": user["display_scores"]["universal"]
	}
	data.append(user_vector)

print("Done. Saving...")
df = pd.DataFrame(data)
df.to_pickle("scores.pkl")

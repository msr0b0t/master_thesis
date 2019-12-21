from pymongo import MongoClient

client = MongoClient()
users_collection = client["thesis-db"].users
tweets_collection = client["thesis-db"].tweets

user_ids = [x["user"]["id_str"] if "user" in x else x["id_str"] for x in users_collection.find({})]

# print(tweets_collection.count_documents({"user.id_str": {"$in": user_ids}})) #2.061.542 tweets

tweets_collection.delete_many({"user.id_str": {"$nin": user_ids}})

from pymongo import MongoClient

def get_retweet_count(tweet):
	return tweet["retweet_count"]

def get_favorite_count(tweet):
	return tweet["favorite_count"]

def is_possibly_sensitive(tweet):
	return tweet.get("possibly_sensitive", False)

def get_media_count(tweet):
	if ("extended_entities" in tweet):
		return len(tweet["extended_entities"]["media"])
	else:
		return 0

def is_duplicate(tweet):
	client = MongoClient()
	tweets_collection = client["thesis-db"].tweets
	duplicate_tweets = tweets_collection.count_documents({"user.id_str": tweet["user"]["id_str"], "text": tweet["text"]})
	return duplicate_tweets > 1

import numpy as np
import pandas as pd
from pymongo import MongoClient
import user_functions as uf


client = MongoClient()
tweets_collection = client["thesis-db"].tweets

user_data = []
tweets = tweets_collection.find({})

for tweet in tweets:
	user = tweet["user"]

	tweet_vector = {
		"tweet_id": tweet["id_str"],
		"author_id": user["id_str"],
		"followers_count": uf.get_followers_count(user),
		"followees_count": uf.get_followees_count(user),
		"followers_to_followees": uf.get_followers_to_followees(user),
		"followees_to_followers": uf.get_followees_to_followers(user),
		"tweets_count": uf.get_tweets_count(user),
		"listed_count": uf.get_listed_count(user),
		"favorites_count": uf.get_favourites_count(user),
		"default_profile": uf.is_default_profile(user),
		"default_profile_image": uf.has_default_profile_image(user),
		"verified": uf.is_verified(user),
		"location": uf.has_location(user),
		"url": uf.has_url(user),
		"description": uf.has_description(user),
		"name_length": uf.get_name_length(user),
		"screen_name_length": uf.get_screen_name_length(user),
		"description_length": uf.get_description_length(user),
		"numerics_in_name_count": uf.get_numbers_count_in_name(user),
		"numerics_in_screen_name_count": uf.get_numbers_count_in_screen_name(user),
		"hashtags_in_name": uf.has_hashtags_in_name(user),
		"hashtags_in_description": uf.has_hashtags_in_description(user),
		"urls_in_description": uf.has_urls_in_description(user),
		"bot_word_in_name": uf.has_bot_word_in_name(user),
		"bot_word_in_screen_name": uf.has_bot_word_in_screen_name(user),
		"bot_word_in_description": uf.has_bot_word_in_description(user),
	}

	user_data.append(tweet_vector)

print("Done. Saving...")
df = pd.DataFrame(user_data)
df.to_pickle("data/user_data.pkl")

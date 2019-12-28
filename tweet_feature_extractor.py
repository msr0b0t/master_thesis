import pandas as pd
from pymongo import MongoClient
import tweet_content_functions as tcf
import tweet_properties_functions as tpf


client = MongoClient()
tweets_collection = client["thesis-db"].tweets

data = []

tweets = tweets_collection.find({})

for tweet in tweets:
	if (tweet["truncated"]):
		text = tweet["extended_tweet"]["full_text"]
	else:
		text = tweet["text"]

	tweet_vector = {
		"tweet_id": tweet["id_str"],
		"author_id": tweet["user"]["id_str"],
		"urls_count": tcf.get_urls_count(text),
		"words_count": tcf.get_words_count(text),
		"tweet_lenght": tcf.get_tweet_length(text),
		"hashtags_count": tcf.get_hashtags_count(text),
		"symbols_count": tcf.get_symbols_count(text),
		"numerics_count": tcf.get_numbers_count(text),
		"mentions_count": tcf.get_mentions_count(text),
		"urls_per_words": tcf.get_urls_per_words(text),
		"hashtags_per_words": tcf.get_hashtags_per_words(text),
		"retweet_count": tpf.get_retweet_count(tweet),
		"favorite_count": tpf.get_favorite_count(tweet),
		"is_possibly_sensitive": tpf.is_possibly_sensitive(tweet),
		"media_count": tpf.get_media_count(tweet),
	}

	data.append(tweet_vector)

print("Done. Saving...")
df = pd.DataFrame(data)
df.to_pickle("data.pkl")

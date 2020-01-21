from functools import reduce
import pandas as pd
import numpy as np
import pickle
import dill
import tweepy
import tweet_content_functions as tcf
import tweet_properties_functions as tpf
import user_functions as uf
from dotenv import load_dotenv
import os
import explain_features as ef

load_dotenv()

auth = tweepy.OAuthHandler(os.getenv("OAUTH_TOKEN"), os.getenv("OAUTH_TOKEN_SECRET"))
auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_TOKEN_SECRET"))
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

df = pd.read_csv("/Users/Mary/Desktop/botwiki-2019.tsv", sep='\t').to_numpy() # TODO: Change this

feature_names = ['favorite_count', 'hashtags_count', 'hashtags_per_words',
				 'is_possibly_sensitive', 'media_count', 'mentions_count',
				 'numerics_count', 'retweet_count', 'symbols_count', 'tweet_lenght',
				 'urls_count', 'urls_per_words', 'words_count',
				 'bot_word_in_description', 'bot_word_in_name',
				 'bot_word_in_screen_name', 'default_profile',
				 'default_profile_image', 'description', 'description_length',
				 'favorites_count', 'followees_count', 'followees_to_followers',
				 'followers_count', 'followers_to_followees',
				 'hashtags_in_description', 'hashtags_in_name', 'listed_count',
				 'location', 'name_length', 'numerics_in_name_count',
				 'numerics_in_screen_name_count', 'screen_name_length',
				 'tweets_count', 'url', 'urls_in_description', 'verified']

data = []
for i, user_row in enumerate(df):
	try:
		print(i)
		timeline = api.user_timeline(user_id=user_row[0], count=10, tweet_mode="extended")

		user = timeline[0].user._json
		user_vector = {
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
			"score": 0 if user_row[1] == "human" else 1
		}
		for tweet in timeline:
			tweet = tweet._json
			text = tweet["full_text"]
			tweet_vector = {
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
				**user_vector,
			}
			data.append(tweet_vector)
	except:
		pass

tweets_df = pd.DataFrame(data)[['favorite_count', 'hashtags_count', 'hashtags_per_words',
								'is_possibly_sensitive', 'media_count', 'mentions_count', 'numerics_count',
								'retweet_count', 'symbols_count', 'tweet_lenght', 'urls_count',
								'urls_per_words', 'words_count', 'bot_word_in_description',
								'bot_word_in_name', 'bot_word_in_screen_name', 'default_profile',
								'default_profile_image', 'description', 'description_length',
								'favorites_count', 'followees_count', 'followees_to_followers',
								'followers_count', 'followers_to_followees', 'hashtags_in_description',
								'hashtags_in_name', 'listed_count', 'location', 'name_length',
								'numerics_in_name_count', 'numerics_in_screen_name_count',
								'screen_name_length', 'tweets_count', 'url', 'urls_in_description',
								'verified', 'score']]
tweets_df.to_pickle("data/botwiki-2019.pkl")  # TODO: Change this

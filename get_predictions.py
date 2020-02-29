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
from collections import Counter
from pymongo import MongoClient

load_dotenv()

client = MongoClient(host=os.getenv("DB_HOST"), port=int(os.getenv("DB_PORT")), username=os.getenv(
	"DB_USERNAME"), password=os.getenv("DB_PASSWORD"), authSource=os.getenv("DB_AUTH_DB"))

db = client["locationuk"]

auth = tweepy.OAuthHandler(os.getenv("OAUTH_TOKEN"),os.getenv("OAUTH_TOKEN_SECRET"))

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

model = pickle.load(open("data/final_best_model_stacking.pkl", 'rb'))
explainer = dill.load(open("data/final_explainer.dill", 'rb'))

def predict(username, user_oauth_token, user_oauth_token_secret):
	auth.set_access_token(user_oauth_token,user_oauth_token_secret)
	api = tweepy.API(auth)

	timeline = api.user_timeline(screen_name=username, count=int(
		os.getenv('TWEET_COUNT', 20)), tweet_mode="extended")
	data = []
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
	}
	tweets_used = []
	for tweet in timeline:
		tweet = tweet._json
		tweets_used.append(db.bot_tweets.insert_one(tweet).inserted_id)
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
									'verified']]
	tweets = tweets_df.to_numpy()

	predictions = []
	positive_features_used_group = []
	negative_features_used_group = []
	for tweet in tweets:
		exp = explainer.explain_instance(
			tweet, model.predict, num_features=len(feature_names))
		predictions.append(exp.predicted_value)
		positive_features_used = * \
			map(lambda x: x[0], filter(lambda x: x[1] > 0, exp.as_map()[1])),
		positive_features_used_group.append(positive_features_used)
		negative_features_used = * \
			map(lambda x: x[0], filter(lambda x: x[1] < 0, exp.as_map()[1])),
		negative_features_used_group.append(negative_features_used)

	positive_feature_count = Counter()
	negative_feature_count = Counter()
	for feat_array in positive_features_used_group:
		positive_feature_count.update(feat_array)
	for feat_array in negative_features_used_group:
		negative_feature_count.update(feat_array)
	positives = np.take(feature_names, [x[0] for x in positive_feature_count.items() if x[1] > 10 ])
	negatives = np.take(feature_names, [x[0] for x in negative_feature_count.items() if x[1] > 10 ])

	features_mean = tweets_df.mean(axis=0).to_dict()

	positive_features = {p: features_mean[p] for p in positives}
	negative_features = {n: features_mean[n] for n in negatives}
	score = float("%.1f" % (int(np.mean(predictions)*10)/float(10)))
	analysis_id = db.bot_predictions.insert_one({
	    "score": score,
	    "tweets_used": tweets_used,
		**ef.explain(positive_features, negative_features)
	}).inserted_id
	return ({"avg_user_score": score, **ef.explain(positive_features, negative_features), "analysis_id": str(analysis_id)})

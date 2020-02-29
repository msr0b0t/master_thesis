import tweepy
from dotenv import load_dotenv
import os
import datetime
import time

load_dotenv()

auth = tweepy.OAuthHandler(os.getenv("OAUTH_TOKEN"),os.getenv("OAUTH_TOKEN_SECRET"))


def convert_twitter_datetime_to_string(date):
	return time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(date,'%a %b %d %H:%M:%S +0000 %Y'))

def convert_string_to_datetime(date):
	return datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")


def get_details(username, user_oauth_token, user_oauth_token_secret):
	auth.set_access_token(user_oauth_token, user_oauth_token_secret)
	api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

	timeline = api.user_timeline(screen_name=username, count=200, contributor_details=False, include_rts=True)

	end_date = datetime.datetime.now()
	start_date = datetime.datetime.now() - datetime.timedelta(days=7)

	user = timeline[0].user._json
	num_of_retweets_by_user = 0
	num_of_tweets_this_week = 0
	monday_to_sunday = [0] * 7
	twelve_am_to_eleven_pm = [0] * 24


	for tweet in timeline:
		tweet = tweet._json
		if ("retweeted_status" in tweet):
			num_of_retweets_by_user += 1
		tweet_time = convert_string_to_datetime(convert_twitter_datetime_to_string(tweet["created_at"]))
		if (tweet_time < end_date and tweet_time > start_date):
			num_of_tweets_this_week += 1
		monday_to_sunday[datetime.datetime.weekday(tweet_time)] += 1
		twelve_am_to_eleven_pm[tweet_time.hour] += 1

	user_data = {
		"image": user["profile_image_url_https"],
		"background_image": user["profile_banner_url"],
		"verified": user["verified"],
		"screen_name": user["screen_name"],
		"display_name": user["name"],
		"description": user["description"],
		"location": user["location"],
		"url": user["url"],
		"date_joined": convert_twitter_datetime_to_string(user["created_at"]),
		"most_recent_post": convert_twitter_datetime_to_string(timeline[0]._json["created_at"]),
		"tweets": user["statuses_count"],
		"following": user["friends_count"],
		"followers": user["followers_count"],
		"likes": user["favourites_count"],
		"lists": user["listed_count"],
		"twitter_user_id": user["id_str"],
		"tweet_language": timeline[0]._json["lang"],
		"tweets_this_week": num_of_tweets_this_week,
		"retweet_ratio": int(num_of_retweets_by_user / 2),
		"tweets_by_day_of_week": monday_to_sunday,
		"tweets_by_hour_of_day": twelve_am_to_eleven_pm,
	}

	return (user_data)

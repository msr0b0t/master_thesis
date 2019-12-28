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

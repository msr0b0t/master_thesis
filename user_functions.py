import re

def get_followers_count(user):
	return user["followers_count"]

def get_followees_count(user):
	return user["friends_count"]

def get_followers_to_followees(user):
	followees = get_followees_count(user)
	if (followees == 0):
		followees = 1
	return get_followers_count(user) / followees

def get_followees_to_followers(user):
	followers = get_followers_count(user)
	if (followers == 0):
		followers = 1
	return get_followees_count(user) / followers

def get_tweets_count(user):
	return user["statuses_count"]

def get_listed_count(user):
	return user["listed_count"]

def get_favourites_count(user):
	return user["favourites_count"]

def is_default_profile(user):
	return user["default_profile"]

def has_default_profile_image(user):
	return user["default_profile_image"]

def is_verified(user):
	return user["verified"]

def has_location(user):
	if (user["location"] == None):
		return False
	else:
		return True

def has_url(user):
	if (user["url"] == None):
		return False
	else:
		return True

def has_description(user):
	if (user["description"] == None):
		return False
	else:
		return True

def get_name_length(user):
	return len(user["name"])

def get_screen_name_length(user):
	return len(user["screen_name"])

def get_description_length(user):
	if (has_description(user)):
		return len(user["description"])
	else:
		return 0

def get_numbers_count_in_name(user):
	numbers = re.findall(r'\d+', user["name"])
	return len(numbers)

def get_numbers_count_in_screen_name(user):
	numbers = re.findall(r'\d+', user["screen_name"])
	return len(numbers)

def has_hashtags_in_name(user):
	hashtags = re.findall(r'#\w*', user["name"])
	return len(hashtags) > 0

def has_hashtags_in_description(user):
	if (has_description(user)):
		hashtags = re.findall(r'#\w*', user["description"])
		return len(hashtags) > 0
	else:
		return False

def has_urls_in_description(user):
	if (has_description(user)):
		urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+] |[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', user["description"])
		return len(urls) > 0
	else:
		return False

def has_bot_word_in_name(user):
	res = re.match(r'bot', user["name"], re.IGNORECASE)
	if (res == None):
		return False
	else:
		return True

def has_bot_word_in_screen_name(user):
	res = re.match(r'bot', user["screen_name"], re.IGNORECASE)
	if (res == None):
		return False
	else:
		return True

def has_bot_word_in_description(user):
	if (has_description(user)):
		res = re.match(r'bot', user["description"], re.IGNORECASE)
		if (res == None):
			return False
		else:
			return True
	else:
		return False

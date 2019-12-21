import re

def get_urls(string):
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+] |[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', string)
    return urls

def get_urls_count(string):
	return len(get_urls(string))

def get_words(string):
	words = string.split()
	return words

def get_words_count(string):
	return len(get_words(string))

def get_tweet_length(string):
	return len(string)

def get_hashtags(string):
	hashtags = re.findall(r'#\w*', string)
	return hashtags

def get_hashtags_count(string):
	return len(get_hashtags(string))

def get_symbols(string):
	symbols = re.findall(r'\W+', string)
	return symbols

def get_symbols_count(string):
	return len(get_symbols(string))

def get_numbers(string):
	numbers = re.findall(r'\d+', string)
	return numbers

def get_numbers_count(string):
	return len(get_numbers(string))

def get_mentions(string):
	mentions = re.findall(r'@\w*', string)
	return mentions

def get_mentions_count(string):
	return len(get_mentions(string))

def get_urls_per_words(string):
	return get_urls_count(string) / get_words_count(string)

def get_hashtags_per_words(string):
	return get_hashtags_count(string) / get_words_count(string)

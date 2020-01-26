def explain(positives, negatives):

	pos = []
	neg = []

	# Is bot because:
	for feature, feature_value in positives.items():
		sentence = ""
		if feature == "is_possibly_sensitive" and feature_value > 0:
			sentence += "This account has tweets with sensitive content. This demonstrates a bot-like behavior."
		elif feature == "default_profile" and feature_value > 0:
			sentence += "This account has a default profile. This is on par with 66% of bots, on average."
		elif feature == "hashtags_in_description" and feature_value > 0:
			sentence += "This account has hashtags in its profile description, which is common in bots. 42% of bot accounts have hashtags in their profile descriptions as well"
		elif feature == "hashtags_in_name" and feature_value > 0:
			sentence += "This account uses hashtags in their name. This is a rare occasion, but, something that is more commonly encountered in bot accounts."
		elif feature == "location" and feature_value < 0.1:
			sentence += "This account does not share their location on their profile. Most non-bot users do."
		elif feature == "url" and feature_value < 0.1:
			sentence += "This account has not set a URL on their profile. Most non-bot users do."
		elif feature == "urls_in_description" and feature_value < 0.1:
			sentence += "This account does not have a URL in their profile's description. Most non-bot users do."
		elif feature == "verified" and feature_value < 0.1:
			sentence += "This account is not verified. While this does not say a lot, if it were, it could increase the certainty that they are not a bot."
		elif feature == "bot_word_in_name" and feature_value > 0:
			sentence += "There are special words in the account's name that indicate a bot-like account (e.g '_bot')."
		elif feature == "bot_word_in_screen_name" and feature_value > 0:
			sentence += "There are special words in the account's screen name that indicate a bot-like account (e.g '_bot')."
		elif feature == "bot_word_in_description" and feature_value > 0:
			sentence += "There are special words in the account's description that indicate a bot-like account (e.g '_bot')."
		elif feature == "favorite_count":
			sentence += "Small average number of favorited tweets. Bots usually have 0.02 favorited tweets on average. This account has " + str(int(feature_value)) + "."
		elif feature == "hashtags_count" and feature_value <= 1.5:
			sentence += "Very low number of hashtags on tweets. Most non-bot accounts have 4.0 hashtags on their tweets on average and this account has " + str(int(feature_value)) + "."
		elif feature == "hashtags_count" and feature_value > 1.5:
			sentence += "Suspicious number of hashtags on tweets. Bots usually have 3.48 hashtags on their tweets and this account has " + str(int(feature_value)) + "."
		elif feature == "hashtags_per_words":
			sentence += "Suspicious amount of hashtags per words in tweets. Bots usually have 0.24 hashtags per words in their tweets and this account has " + str(round(feature_value)) + "."
		elif feature == "media_count":
			sentence += "This account rarely adds media in their tweets ( " + str(round(feature_value, 2)) + " per tweet ). This is on par with bot-like accounts, who have, on average, 0.02."
		elif feature == "mentions_count" and feature_value > 0.5:
			sentence += "This account mentions other accounts frequently. ( " + str(round(feature_value, 2)) + " accounts per tweet). Bots usually have 0.87 mentions in their tweets, on average."
		elif feature == "numerics_count":
			sentence += "This account uses numeric characters frequently. ( " + str(round(feature_value, 2)) + " characters per tweet). Bots usually have 1.66 numeric characters per tweet, on average."
		elif feature == "retweet_count":
			sentence += "Small number of retweets indicates that a tweet is more probable to have been produced by a bot account."
		elif feature == "symbols_count":
			sentence += "This account uses symbols frequently. ( " + str(round(feature_value, 2)) + " symbols per tweet). Bots usually have 21.2 symbols per tweet, on average."
		elif feature == "tweet_lenght":
			sentence += "Suspicious average number of characters per tweet ( " + str(round(feature_value, 2)) + " ). Bots usually have 143.7 characters on their tweets."
		elif feature == "urls_count":
			sentence += "Suspicious average number of URLs per tweet ( " + str(round(feature_value, 2)) + " ). Bots usually have 0.55 URLs per tweet."
		elif feature == "urls_per_words" and feature_value >= 0.02:
			sentence += "This account's URL per word ratio for each tweet, is suspiciously high."
		elif feature == "words_count" and feature_value >= 19:
			sentence += "This account's tweets are very big in length ( " + str(round(feature_value)) + " ). Non-bots usually tweet small pieces of text."
		elif feature == "description_length" and feature_value < 64:
			sentence += "This account's description is very small in length ( " + str(round(feature_value)) + " ). Bots have less than 63.2 characters on their description, on average."
		elif feature == "favorites_count" and feature_value < 3610:
			sentence += "Low number of tweets the account has favorited ( " + str(round(feature_value)) + " ). Non bots usually favorite 6224 tweets on average."
		elif feature == "favorites_count" and feature_value > 3610:
			sentence += "Large number of tweets the account has favorited ( " + str(round(feature_value)) + " ). Bots usually favorite 3609 tweets on average."
		elif feature == "followees_count":
			sentence += "Suspicious number of followees ( " + str(round(feature_value)) + " ). Bots usually follow 3658 accounts on average."
		elif feature == "followees_to_followers" and feature_value > 2:
			sentence += "This account's followees to followers ratio is suspiciously high ( " + str(round(feature_value, 2)) + " ). Bots usually have 3.91 followees per followers, on average."
		elif feature == "followers_count":
			sentence += "Suspicious number of followers ( " + str(round(feature_value)) + " ). Bots usually are followed by 3469 accounts on average."
		elif feature == "followers_to_followees":
			sentence += "This account's followers to followees ratio is suspiciously low ( " + str(round(feature_value, 2)) + " ). Bots usually have 34.58 followers per followees, on average."
		elif feature == "listed_count" and feature_value < 30:
			sentence += "This account is not a member of many lists. Most non-bot users belong to lots of lists. This account belongs to " + str(round(feature_value)) + "lists."
		elif feature == "name_length":
			sentence += "This account's name length is suspicious ( " + str(round(feature_value)) + " characters ). Bots have 12.3 characters on their name, on average."
		elif feature == "numerics_in_name_count":
			sentence += "This account's number of numeric characters in their name is suspicious ( " + str(round(feature_value)) + " characters )."
		elif feature == "numerics_in_screen_name_count":
			sentence += "This account's number of numeric characters in their screen name is suspicious ( " + str(round(feature_value)) + " characters )."
		elif feature == "screen_name_length":
			sentence += "This account's screen name length is suspicious ( " + str(round(feature_value)) + " characters ). Bots have 11.3 characters on their name, on average."
		elif feature == "tweets_count":
			sentence += "This account's number of tweets is not as large as most non-bot accounts. This occurs either in bot-like accounts or newly created accounts."

		if (len(sentence) > 0): pos.append(sentence)

	# Is NOT bot because:
	for feature, feature_value in negatives.items():
		sentence = ""
		if feature == "is_possibly_sensitive" and feature_value < 0.1:
			sentence += "This account does not have tweets with sensitive content. Most bot accounts do."
		elif feature == "default_profile" and feature_value < 0.1:
			sentence += "This account does not have a default profile, when 66% of bots, on average, have."
		elif feature == "hashtags_in_description" and feature_value < 0.1:
			sentence += "This account does not have hashtags in its profile description. Only 31% of non bot accounts have hashtags in their profile descriptions."
		elif feature == "hashtags_in_name" and feature_value < 0.1:
			sentence += "This account does not use hashtags in their name. This is more commonly encountered in bot accounts."
		elif feature == "location" and feature_value > 0:
			sentence += "This account shares their location on their profile. Most bot accounts do not."
		elif feature == "url" and feature_value > 0:
			sentence += "This account has set a URL on their profile. Most bot accounts do not."
		elif feature == "urls_in_description" and feature_value > 0:
			sentence += "This account has a URL in their profile's description. Most bot accounts do not."
		elif feature == "verified" and feature_value > 0:
			sentence += "This account is verified. Almost always, this means that the account belongs to a non-bot user."
		elif feature == "favorite_count":
			sentence += "Normal average number of favorited tweets. Bots usually have 0.02 favorited tweets on average. This account has " + str(int(feature_value)) + "."
		elif feature == "hashtags_count":
			sentence += "Normal number of hashtags on tweets. Bots usually have 3.48 hashtags on their tweets and this account has " + str(int(feature_value)) + "."
		elif feature == "hashtags_per_words":
			sentence += "Normal amount of hashtags per words in tweets. Bots usually have 0.24 hashtags per words in their tweets and this account has " + str(round(feature_value)) + "."
		elif feature == "media_count":
			sentence += "This account often adds media in their tweets ( " + str(round(feature_value, 2)) + " per tweet ). This is not on par with bot-like accounts, who have, on average, 0.02."
		elif feature == "mentions_count" and feature_value <= 0.5:
			sentence += "This account mentions other accounts rarely. ( " + str(round(feature_value, 2)) + " accounts per tweet). Bots usually have 0.87 mentions in their tweets, on average."
		elif feature == "numerics_count":
			sentence += "This account uses numeric characters rarely. ( " + str(round(feature_value, 2)) + " characters per tweet). Bots usually have 1.66 numeric characters per tweet, on average."
		elif feature == "retweet_count":
			sentence += "Big number of retweets indicates that a tweet is more probable to have been produced by a non-bot account."
		elif feature == "symbols_count":
			sentence += "This account uses symbols rarely. ( " + str(round(feature_value, 2)) + " symbols per tweet). Bots usually have 21.2 symbols per tweet, on average."
		elif feature == "tweet_lenght":
			sentence += "Normal average number of characters per tweet ( " + str(round(feature_value, 2)) + " ). Bots usually have 143.7 characters on their tweets."
		elif feature == "urls_count":
			sentence += "Normal average number of URLs per tweet ( " + str(round(feature_value, 2)) + " ). Bots usually have 0.55 URLs per tweet."
		elif feature == "urls_per_words" and feature_value < 0.02:
			sentence += "This account's URL per word ratio for each tweet is low, which is normal."
		elif feature == "words_count" and feature_value < 19:
			sentence += "This account's tweets are rather small in length ( " + str(round(feature_value)) + " ). Non-bots, usually tweet small pieces of text."
		elif feature == "description_length":
			sentence += "This account's description is average in length ( " + str(round(feature_value)) + " ). Bots have 63.2 characters on their description, on average."
		elif feature == "favorites_count" > 3610 :
			sentence += "Normal average number of tweets the account has favorited ( " + str(round(feature_value)) + " ). Non bots usually favorite 6224 tweets on average."
		elif feature == "followees_count":
			sentence += "Average number of followees ( " + str(round(feature_value)) + " ). Bots usually follow 3658 accounts on average."
		elif feature == "followees_to_followers" and feature_value < 2:
			sentence += "This account's followees to followers ratio is not very high ( " + str(round(feature_value, 2)) + " ), which is normal. Bots usually have 3.91 followees per followers, on average."
		elif feature == "followers_count":
			sentence += "Average number of followers ( " + str(round(feature_value)) + " ). Bots usually are followed by 3469 accounts on average."
		elif feature == "followers_to_followees" and feature_value <= 34:
			sentence += "This account's followers to followees ratio is low ( " + str(round(feature_value, 2)) + " ), which is normal. Bots usually have 34.58 followers per followees, on average."
		elif feature == "followers_to_followees" and feature_value > 34:
			sentence += "This account's followers to followees ratio is rather high ( " + str(round(feature_value, 2)) + " ), which is normal. Non bots usually have more than 90.99 followers per followees, on average."
		elif feature == "listed_count" and feature_value >= 30:
			sentence += "This account is a member of many lists, which is normal for non-bot users. This account belongs to " + str(round(feature_value)) + "lists."
		elif feature == "name_length":
			sentence += "This account's name length is normal ( " + str(round(feature_value)) + " characters ). Bots have 12.3 characters on their name, on average."
		elif feature == "numerics_in_name_count":
			sentence += "This account's number of numeric characters in their name is normal ( " + str(round(feature_value)) + " characters )."
		elif feature == "numerics_in_screen_name_count":
			sentence += "This account's number of numeric characters in their screen name is normal ( " + str(round(feature_value)) + " characters )."
		elif feature == "screen_name_length":
			sentence += "This account's screen name length is normal ( " + str(round(feature_value)) + " characters ). Bots have 11.3 characters on their name, on average."
		elif feature == "tweets_count":
			sentence += "This account's number of tweets is rather large. This occurs mostly in non-bot accounts."

		if (len(sentence) > 0): neg.append(sentence)

	return ({"pos": pos, "neg": neg})

import pandas as pd


data = pd.read_pickle("data/data.pkl")
user_data = pd.read_pickle("data/user_data.pkl").drop(["author_id"], axis=1)
scores = pd.read_pickle("data/scores.pkl")

all_data = pd.merge(data, user_data, on="tweet_id")
dataset = pd.merge(all_data, scores, on="author_id")

dataset.to_pickle("data/dataset.pkl")

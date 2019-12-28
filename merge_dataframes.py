import pandas as pd


data = pd.read_pickle("data.pkl")
scores = pd.read_pickle("scores.pkl")

dataset = pd.merge(data, scores, on="author_id")

dataset.to_pickle("dataset.pkl")

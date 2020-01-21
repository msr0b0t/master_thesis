import pandas as pd
import numpy as np
import pickle
from sklearn.metrics import f1_score


dataset = pd.read_pickle("data/second_dataset.pkl").drop(["score", "author_id", "tweet_id"], axis=1, errors="ignore")
dataset = pd.concat(np.array_split(dataset, np.ceil(len(dataset) / 5))[1::2])


model = pickle.load(open("data/best_classification_model_random_forest.pkl", 'rb'))

predictions = [x[1] * 5 for x in model.predict_proba(dataset.to_numpy())]


dataset = dataset.assign(score = predictions)

dataset.to_pickle("data/regression_dataset.pkl")

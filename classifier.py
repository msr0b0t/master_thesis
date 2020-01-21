import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

dataset = pd.read_pickle("data/second_dataset.pkl")
dataset = pd.concat(np.array_split(dataset, np.ceil(len(dataset) / 5))[::2])

X = dataset.drop(["score", "author_id", "tweet_id"], axis=1, errors="ignore").to_numpy()
y = dataset[["score"]].values.ravel()

# Train a RandomForest classifier
print("#################### RANDOM FOREST ####################")
parameters = {
    "max_depth": [5, 10, 13, None], # None
    "n_estimators": [i for i in range(100, 200, 10)], # 100
}

model = GridSearchCV(RandomForestClassifier(random_state=14, n_jobs=-1),
                     parameters, n_jobs=-1, scoring='f1', verbose=True, cv=5)
model.fit(X, y)
# Print the evaluation results
print("F1 Score", model.best_score_)  # 0.8435415774332122
print(model.best_estimator_)
print()
pickle.dump(model.best_estimator_, open("data/best_classification_model_random_forest.pkl", 'wb'))

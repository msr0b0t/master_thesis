import pandas as pd
import pickle
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV

dataset = pd.read_pickle("data/final_dataset.pkl")
dataset = dataset[dataset.score < 5]

X = dataset.drop(["score", "author_id", "tweet_id"], axis=1, errors="ignore").to_numpy()
y = dataset[["score"]].values.ravel()

# Train a RandomForest regressor
print("#################### RANDOM FOREST ####################")
parameters = {
    "max_depth": [5, 10, 13, None],
    "n_estimators": [i for i in range(100, 200, 10)],
}

model = GridSearchCV(RandomForestRegressor(random_state=14, n_jobs=-1),
                     parameters, n_jobs=-1, scoring='neg_mean_squared_error', verbose=True, cv=5)
model.fit(X, y)
# Print the evaluation results
print("MSError", model.best_score_) # -0.9421567767326771
print(model.best_estimator_)
print()
pickle.dump(model.best_estimator_, open("data/final_best_model_random_forest.pkl", 'wb'))

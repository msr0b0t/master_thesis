import pandas as pd
import pickle
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import GridSearchCV

dataset = pd.read_pickle("data/dataset.pkl")
dataset = dataset[dataset.score < 5].head(200000)

X = dataset.drop(["score", "author_id", "tweet_id"], axis=1)
y = dataset[["score"]].values.ravel()

# Train a RandomForest regressor
print("#################### TRADITIONAL GBOOST ####################")
parameters = {
    "max_depth": [4],
    "n_estimators": [100],
}

model = GridSearchCV(GradientBoostingRegressor(random_state=14),
                     parameters, n_jobs=-1, scoring='neg_mean_squared_error', verbose=True, cv=5)
model.fit(X, y)
# Print the evaluation results
print("MSError", model.best_score_) # -0.9226590276627384
print(model.best_estimator_)
print()
# pickle.dump(model.best_estimator_, open("data/best_model_random_forest.pkl", 'wb'))

import pandas as pd
import pickle
from sklearn.experimental import enable_hist_gradient_boosting
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import GridSearchCV

dataset = pd.read_pickle("data/final_dataset.pkl")
dataset = dataset[dataset.score < 5]

X = dataset.drop(["score", "author_id", "tweet_id"], axis=1, errors="ignore").to_numpy()
y = dataset[["score"]].values.ravel()

# Train a HistGradientBoosting regressor
print("#################### GBOOST ####################")
parameters = {
    "max_depth": [5, 10, 13, None],
    "l2_regularization": [0, 1, 2]
}

model = GridSearchCV(HistGradientBoostingRegressor(random_state=14),
                     parameters, n_jobs=-1, scoring='neg_mean_squared_error', verbose=True, cv=5)
model.fit(X, y)
# Print the evaluation results
print("MSError", model.best_score_) # -0.7848931269873645
print(model.best_estimator_)
print()
pickle.dump(model.best_estimator_, open("data/final_best_model_gradient_boosting.pkl", 'wb'))

import pandas as pd
import pickle
from sklearn.experimental import enable_hist_gradient_boosting
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor, StackingRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import RidgeCV

dataset = pd.read_pickle("data/final_dataset.pkl")
dataset = dataset[dataset.score < 5]

X = dataset.drop(["score", "author_id", "tweet_id"], axis=1, errors="ignore").to_numpy()
y = dataset[["score"]].values.ravel()

# Train a Stacking regressor
print("#################### STACKING ####################")
estimators = [
    ("Random Forest", RandomForestRegressor(random_state=14, n_jobs=-1, max_depth=13)),
    ("Gradient Boosting", HistGradientBoostingRegressor(random_state=14, l2_regularization=1))
]
model = StackingRegressor(estimators=estimators, final_estimator=RidgeCV(), n_jobs=-1)
model.fit(X, y)

# Print the evaluation results
print("MSError", model.score(X, y)) # 0.6033506428465925
print(model)
print()
pickle.dump(model, open("data/final_best_model_stacking.pkl", 'wb'))

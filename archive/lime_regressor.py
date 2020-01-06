import sklearn.ensemble
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

dataset =  pd.read_pickle("data/dataset.pkl").head(5)

# dc = dataset.columns



# print(categorical_features)

# exit()

dataset = pd.read_pickle("data/dataset.pkl").head(5000)

X = dataset.drop(["score", "author_id", "tweet_id"], axis=1)
y = dataset[["score"]].values.ravel()

model = sklearn.ensemble.RandomForestRegressor(n_estimators=1000)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=14)

model.fit(X_train, y_train)

print("Random Forest MSError", np.mean((model.predict(X_test) - y_test) ** 2))

print("MSError when predicting the mean", np.mean((y_train.mean() - y_test) ** 2))


categorical_features = [4, 15, 16, 17, 18, 19, 20, 27, 28, 30, 36, 37, 38]

import lime
import lime.lime_tabular

explainer = lime.lime_tabular.LimeTabularExplainer(X_train.to_numpy(), feature_names=list(X.columns.values), class_names=["score"], categorical_features=categorical_features, verbose=True, mode="regression")

exp = explainer.explain_instance(X_test.to_numpy()[25], model.predict, num_features=len(list(X.columns)))

exp.show_in_notebook(show_table=True)
exp.save_to_file('image.html')

exp.as_list()

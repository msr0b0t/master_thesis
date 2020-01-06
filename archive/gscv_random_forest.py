import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split, GridSearchCV

dataset = pd.read_pickle("data/dataset.pkl").head(5000)

X = dataset.drop(["score", "author_id", "tweet_id"], axis=1)
y = dataset[["score"]].values.ravel()

# Split the input dataset in order to evaluate our resutls
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=14)

# Train a RandomForest classifier, using the Binary Relevance dataset transormation method
parameters = {
	"n_estimators": [130],
}

model = GridSearchCV(RandomForestRegressor(random_state=14, n_jobs=-1, max_depth=13), parameters, n_jobs=-1, verbose=True, cv=5) #0.466
model.fit(X_train, y_train)

# Print the evaluation results
print(model.best_estimator_.score(X_test, y_test))
print(model.best_estimator_)

# Make predictions using the testing set
y_pred = model.best_estimator_.predict(X_test)

# Plot outputs
plt.scatter(X_test, y_test,  color='black')
plt.plot(X_test, y_pred, color='blue', linewidth=3)
plt.xticks(())
plt.yticks(())
plt.show()

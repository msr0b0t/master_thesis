from sklearn.ensemble import StackingRegressor
from sklearn.model_selection import cross_validate, cross_val_predict, train_test_split
import pandas as pd
import numpy as np
import time
from sklearn.linear_model import RidgeCV
from sklearn.linear_model import LassoCV
from sklearn.experimental import enable_hist_gradient_boosting  # noqa
from sklearn.ensemble import HistGradientBoostingRegressor, RandomForestRegressor
import matplotlib.pyplot as plt
import pickle


def plot_regression_results(ax, y_true, y_pred, title, scores, elapsed_time):
    """Scatter plot of the predicted vs true targets."""
    ax.plot([y_true.min(), y_true.max()],
            [y_true.min(), y_true.max()],
            "--r", linewidth=2)
    ax.scatter(y_true, y_pred, alpha=0.2)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.spines["left"].set_position(("outward", 10))
    ax.spines["bottom"].set_position(("outward", 10))
    ax.set_xlim([0, 5])
    ax.set_ylim([0, 5])
    ax.set_xlabel("Measured")
    ax.set_ylabel("Predicted")
    title = "Stacking Prediction Results"
    ax.set_title(title)


from sklearn.experimental import enable_hist_gradient_boosting  # noqa

# model = pickle.load(open("../data/best_model_random_forest.pkl", 'rb'))
# model = pickle.load(open("../data/best_model_gradient_boosting.pkl", 'rb'))
model = pickle.load(open("../data/best_model_stacking.pkl", 'rb'))

dataset = pd.read_pickle("../data/dataset.pkl").head(200000)
dataset = dataset[dataset.score < 5]


X = dataset.drop(["score", "author_id", "tweet_id"], axis=1).to_numpy()
y = dataset[["score"]].values.ravel()

fig = plt.figure()
ax = plt.gca()

start_time = time.time()
score = 0.7733633944660586
elapsed_time = time.time() - start_time

y_pred = model.predict(X)
plot_regression_results(
    ax, y, y_pred,
    "Stacking Regressor",
    (r"$MSE={:.2f}$")
    .format(score),
    elapsed_time)

plt.tight_layout()
plt.show()

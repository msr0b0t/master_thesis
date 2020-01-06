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
    ax.set_xlim([y_true.min(), y_true.max()])
    ax.set_ylim([y_true.min(), y_true.max()])
    ax.set_xlabel("Measured")
    ax.set_ylabel("Predicted")
    extra = plt.Rectangle((0, 0), 0, 0, fc="w", fill=False,
                          edgecolor="none", linewidth=0)
    ax.legend([extra], [scores], loc="upper left")
    title = title + "\n Evaluation in {:.2f} seconds".format(elapsed_time)
    ax.set_title(title)


from sklearn.experimental import enable_hist_gradient_boosting  # noqa

model = pickle.load(open("best_model.pkl", 'rb'))

dataset = pd.read_pickle("dataset.pkl").head(20000)
dataset = dataset[dataset.score < 5]


X = dataset.drop(["score", "author_id", "tweet_id"], axis=1).to_numpy()
y = dataset[["score"]].values.ravel()

fig = plt.figure()
ax = plt.gca()

start_time = time.time()
score = cross_validate(model, X, y,
                       scoring=["r2", "neg_mean_absolute_error"],
                       n_jobs=-1, verbose=0)
elapsed_time = time.time() - start_time

y_pred = cross_val_predict(model, X, y, n_jobs=-1, verbose=0)
plot_regression_results(
    ax, y, y_pred,
    "Stacking Regressor",
    (r"$R^2={:.2f} \pm {:.2f}$" + "\n" + r"$MAE={:.2f} \pm {:.2f}$")
    .format(np.mean(score["test_r2"]),
            np.std(score["test_r2"]),
            -np.mean(score["test_neg_mean_absolute_error"]),
            np.std(score["test_neg_mean_absolute_error"])),
    elapsed_time)


plt.suptitle("Single predictors versus stacked predictors")
plt.tight_layout()
plt.show()

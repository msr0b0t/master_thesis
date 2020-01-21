import pandas as pd
import dill
from lime.lime_tabular import LimeTabularExplainer


dataset = pd.read_pickle("data/final_dataset.pkl")
X = dataset.drop(["score", "author_id", "tweet_id"], axis=1, errors="ignore")
y = dataset[["score"]].values.ravel()

categorical_features = [4, 15, 16, 17, 18, 19, 20, 27, 28, 30, 36, 37, 38]
explainer = LimeTabularExplainer(X.to_numpy(), feature_names=list(
    X.columns.values), class_names=["score"], categorical_features=categorical_features, verbose=True, mode="regression")

# Note: To later load it use: explainer = dill.load(open("explainer.dill", 'rb'))
dill.dump(explainer, open("data/final_explainer.dill", 'wb'))

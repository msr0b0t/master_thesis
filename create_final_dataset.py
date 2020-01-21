import pandas as pd


df1 = pd.read_pickle("data/regression_dataset.pkl") # 8775
df2 = pd.read_pickle("data/dataset.pkl")

dataset = df1.append([df2], sort=False)

dataset.to_pickle("data/final_dataset.pkl")

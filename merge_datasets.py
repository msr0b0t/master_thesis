import pandas as pd


df1 = pd.read_pickle("data/cresci-rtbust-2019.pkl")
df2 = pd.read_pickle("data/botometer-feedback-2019.pkl")
df3 = pd.read_pickle("data/botwiki-2019.pkl")

dataset = df1.append([df2, df3])

dataset.to_pickle("data/second_dataset.pkl")

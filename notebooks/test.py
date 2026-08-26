import pandas as pd

df1 = pd.read_csv("data/claims.csv")
df2 = pd.read_csv("data/plans.csv")

df1.info()
df1.head()

df2.info()
df2.head()

df1 = df1.drop_duplicates()
df2 = df2.drop_duplicates()

df1 = df1.dropna()
df2 = df2.dropna()

df1["date_filed"] = pd.to_datetime(df1["date_filed"], errors="coerce")
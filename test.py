import pandas as pd
from sklearn.preprocessing import LabelEncoder


file_path = "output/session 2.csv"
df = pd.read_csv(file_path)

# activities = df["activity"].unique()
#
# labels = ['a', 'b', 'c']
# encoder = LabelEncoder()
# encoder.fit(labels)
# for i, item in enumerate(encoder.classes_):
#     print(item, '=> ', i)
# *--------------------------------------------------

x = df.iloc[:, :].values
encoder = LabelEncoder()
x[:, 2] = encoder.fit_transform((x[:, 2]))
y = pd.DataFrame(x)
df.to_csv(r'test.csv', index=False)
# print(df["activity"])
# print(y[2])
print(df.head())
df["activity"] = y[2]
print(df.head())
df.to_csv(file_path)
# ------------------------------------

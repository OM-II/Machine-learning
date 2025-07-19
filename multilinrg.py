import pandas as pd
data=pd.read_csv("multiple_linear_regression_dataset.csv")
print(data.head())
print(data.columns)
print(data.isna())
print(data.describe())

#
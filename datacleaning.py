import pandas as pd 
data=pd.read_csv("xAPI-Edu-Data.csv")
#pirnt categorical dataset
cd=data.select_dtypes(include=['object','category']).columns
print("categorical data from dataset",cd)
#print numeric data only from dataset
nd=data.select_dtypes(include=['number']).columns
print("numeric data from dataset ",nd)
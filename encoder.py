import sklearn
import pandas as pd
import numpy as np
from sklearn.preprocessing import nomial
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
data=pd.read_csv("xAPI-Edu-Data.csv")
print(data.head())
cd = data.select_dtypes(include=['object', 'category']).columns
print(cd)
nd=data.select_dtypes(include='number').columns
print(nd)
print(data.isna().sum())
#csutomized a data (specific columns and row )
csd=data.iloc[:,[0,6,7,14,15,16,11]]
csd=csd.iloc[:,[0,1,3]]
print(csd)
x=csd.drop("ParentschoolSatisfaction",axis=1)
y=csd["ParentschoolSatisfaction"]
print(x)
print(y)
#spliting data set 
xtrain,xtest,ytrain,ytest=train_test_split(x,y,test_size=0.2,random_state=42)
or=OrdinalEncoder(categories=[[""]])
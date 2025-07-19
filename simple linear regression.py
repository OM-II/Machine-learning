import pandas as pd
import numpy as np
import sklearn
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

data =pd.read_csv("Salary_Data.csv")
#print(data.head(),"\n",data.describe())
#print(data.columns.tolist())
print(data.isna().sum())
x=data.iloc[:,[0]]
y= data.iloc[:,-1]
x_train,x_test,y_train,y_test= train_test_split(x,y,test_size=0.2,random_state=2)
LR= LinearRegression()
LR.fit(x_train,y_train)
print(x_test)
print(y_test)
print(data)
ypredict = LR.predict(x_test.iloc[1].values.reshape(1,1)) # value which is at index 1 and covert its value in 2d array
print("prediction for " ,x_test.iloc[1] ,"is ",ypredict)# prediction
print("actual output should be",y_test.iloc[1]) 
print(x_test.iloc[1],y_test.iloc[1])   # print the value which is used for testing from feature column and its actual output

#fit line
plt.scatter(data['YearsExperience'],data['Salary'])
plt.plot(x_train,LR.predict(x_train),color="red")
plt.xlabel("Experience")
plt.ylabel("Salary")
plt.show()
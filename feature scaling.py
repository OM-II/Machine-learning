import seaborn as sns
import sklearn 
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
data=sns.load_dataset("iris")
data= data.drop("species",axis=1)
print(data.head())
#scaling=MinMaxScaler()
#print("after normalization value between o to 1", scaling.fit_transform(data[["sepal_length","petal_width"]]))
scale=StandardScaler()
print("after standardization",scale.fit_transform(data[["sepal_length","petal_width"]]))
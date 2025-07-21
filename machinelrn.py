# 1. Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.feature_selection import VarianceThreshold
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, ConfusionMatrixDisplay

# 2. Load Dataset
df = pd.read_csv("your_data.csv")  # Replace with your dataset path

# 3. Basic EDA
print(df.head())
print(df.describe())
print(df.info())
print("Missing Values:\n", df.isnull().sum())

# 4. Define Features and Target
X = df.drop("target", axis=1)  # Replace 'target' with your actual target column
y = df["target"]

# 5. Identify Column Types
numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_cols = X.select_dtypes(include=['object']).columns.tolist()

# 6. Ordinal and Nominal Columns (example)
ordinal_cols = ['education']  # Replace as needed
ordinal_categories = [["High School", "Bachelor", "Master", "PhD"]]
nominal_cols = list(set(categorical_cols) - set(ordinal_cols))

# 7. Transformers
numeric_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="mean")),
    ("scaler", StandardScaler()),
    ("selector", VarianceThreshold(threshold=0.01))
])

ordinal_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OrdinalEncoder(categories=ordinal_categories))
])

nominal_transformer = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore", sparse=False))
])

# 8. Preprocessing
preprocessor = ColumnTransformer([
    ("num", numeric_transformer, numeric_cols),
    ("ord", ordinal_transformer, ordinal_cols),
    ("nom", nominal_transformer, nominal_cols)
])

# 9. Define Base Models
rf = RandomForestClassifier(n_estimators=100, random_state=42)
gb = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, random_state=42)

# 10. Voting Classifier (Ensemble)
ensemble_model = VotingClassifier(estimators=[
    ("rf", rf),
    ("gb", gb)
], voting='soft')  # 'soft' uses predicted probabilities

# 11. Build Final Pipeline
pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", ensemble_model)
])

# 12. Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 13. Cross-validation
cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5)
print("Cross-validation scores:", cv_scores)
print("CV Mean Accuracy:", np.mean(cv_scores))

# 14. Fit the Model
pipeline.fit(X_train, y_train)

# 15. Predictions & Evaluation
y_pred = pipeline.predict(X_test)

print("\nTest Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred, average="macro"))
print("Recall:", recall_score(y_test, y_pred, average="macro"))
print("F1 Score:", f1_score(y_test, y_pred, average="macro"))

# 16. Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
ConfusionMatrixDisplay(cm).plot(cmap="Blues")
plt.title("Confusion Matrix")
plt.show()

# 17. Feature Importance from Random Forest
# Get feature names from preprocessing
feature_names = pipeline.named_steps['preprocessor'].get_feature_names_out()
rf_model = pipeline.named_steps['classifier'].named_estimators_['rf']
importances = rf_model.feature_importances_

# Top 10 Important Features
feat_imp = pd.Series(importances, index=feature_names).sort_values(ascending=False)
feat_imp.head(10).plot(kind='barh', title='Top 10 Important Features (RF)', color='coral')
plt.xlabel("Feature Importance Score")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

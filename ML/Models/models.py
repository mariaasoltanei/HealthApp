import pandas as pd
import os
from concrete.ml.sklearn import LinearRegression, LogisticRegression, NeuralNetClassifier, RandomForestClassifier, DecisionTreeClassifier, LinearSVC
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import make_pipeline
from torch import nn
notebook_dir = os.getcwd()
data_dir = os.path.abspath(os.path.join(notebook_dir, "ML"))


train_df = pd.read_csv("/Users/mariaasoltanei/Desktop/FACULTATE/CERCETARE/HealthApp/ML/Models/train.csv")
test_df = pd.read_csv("/Users/mariaasoltanei/Desktop/FACULTATE/CERCETARE/HealthApp/ML/Models/test.csv")

X_train = train_df.drop(columns=['Activity', 'ActivityName'])
y_train = train_df['Activity']
print(y_train)
X_test = test_df
# Scale your features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train).astype("float32")
X_test_scaled = scaler.transform(X_test).astype("float32")

label_encoder = LabelEncoder()
y_train_encoded = label_encoder.fit_transform(y_train)
# print(y_train_encoded)

def get_model(name="LinearSVC"):
    if name == "LinearSVC":
        return LinearSVC(C=30, dual=False, penalty ='l2')
    elif name == "LogisticRegression":
        return LogisticRegression(n_bits=8)
    elif name == "RandomForestClassifier":
        return RandomForestClassifier(n_bits=8, n_estimators=10, max_depth=5)
    else:
        raise ValueError(f"Unknown model: {name}")

model = LinearSVC(n_bits=3, C=0.01, tol=1e-8)
model.fit(X_train_scaled, y_train_encoded)

# Clear prediction
y_pred_clear = model.predict(X_test_scaled)
print("Predictions (Clear):", y_pred_clear)

# Compile and predict using FHE
model.compile(X_test_scaled)
y_pred = model.predict(X_test_scaled, fhe="execute")
print("Predictions (FHE):", y_pred)

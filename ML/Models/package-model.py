import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
from sklearn.svm import LinearSVC
# Load training data
df = pd.read_csv("/Users/mariaasoltanei/Desktop/FACULTATE/CERCETARE/HealthApp/ML/TestDataProcesing/CSVs/train.csv")

# Separate features and labels
X = df.drop(columns=["Activity", "ActivityName"])
y = df["ActivityName"]

# Train model
model = LinearSVC(C=0.01, penalty="l2", tol=1e-8)
model.fit(X, y)

# Save model to disk
joblib.dump(model, "./lsvc_model.pkl")
print("✅ Model saved as rf_model.pkl")

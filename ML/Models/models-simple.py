import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC, LinearSVC

# === Load Data ===
train_df = pd.read_csv("/Users/mariaasoltanei/Desktop/FACULTATE/CERCETARE/HealthApp/ML/TestDataProcesing/CSVs/train.csv")
test_df = pd.read_csv("/Users/mariaasoltanei/Desktop/FACULTATE/CERCETARE/HealthApp/ML/TestDataProcesing/CSVs/test.csv")


# === Prepare Data ===
X_train = train_df.drop(columns=["Activity", "ActivityName"])
y_train = train_df["Activity"]

X_test = test_df.copy()

# === Train Model ===
models = {
    "Random Forest": RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42),
    # # "Logistic Regression": LogisticRegression(max_iter=1000),
    # "Decision Tree": DecisionTreeClassifier(),
    # "SVM": SVC(gamma='scale', probability=True),

    "LinearSVC": LinearSVC(C=0.01, penalty="l2", tol=1e-8),
}

# === Train + Predict ===
print("📊 Model Predictions (first 10 test samples):\n")

for name, model in models.items():
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    print(f"{name}: {list(predictions)}")
    print("--------------------------------------------------")
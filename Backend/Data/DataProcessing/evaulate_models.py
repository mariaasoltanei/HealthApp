import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC


# === CONFIG ===
train_path = "/Users/mariaasoltanei/Desktop/FACULTATE/CERCETARE/HealthApp/Backend/Data/DataProcessing/train_features.csv"
test_path = "/Users/mariaasoltanei/Desktop/FACULTATE/CERCETARE/HealthApp/Backend/Data/DataProcessing/test_features.csv"  # Assuming no labels in test

# === LOAD DATA ===
train_df = pd.read_csv(train_path)
X_train = train_df.drop(columns=["Activity"])
y_train = train_df["Activity"]

X_test = pd.read_csv(test_path)

# === STANDARDIZE FEATURES ===
# scaler = StandardScaler()
# X_train_scaled = scaler.fit_transform(X_train)
# X_test_scaled = scaler.transform(X_test)

# === CLASSIFIERS ===
models = {
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "KNN (k=5)": KNeighborsClassifier(n_neighbors=5),
    "LinearSVC": LinearSVC(C=0.01, penalty='l2', tol=1e-5),
}

# === TRAIN & PREDICT ===
for name, model in models.items():
    print(f"\n🔍 {name}")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    activity_map = {
        1: "WALKING",
        2: "WALKING_UPSTAIRS",
        3: "WALKING_DOWNSTAIRS",
        4: "SITTING",
        5: "STANDING",
        6: "LAYING"
    }
    y_pred_named = [activity_map[label] for label in y_pred]

    # Print predicted activities
    print("📋 Predicted activities (named):")
    print(y_pred_named)

    # 📌 NOTE: Only use this if your test data is labeled
    # y_test = pd.read_csv("true_labels.csv")["activity"]
    # print(classification_report(y_test, y_pred))

    # Just show predicted class distribution (no test labels available)
    preds = pd.Series(y_pred).value_counts().sort_index()
    print("Predicted activity counts:", preds.to_dict())

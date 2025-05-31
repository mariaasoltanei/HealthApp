import pandas as pd
from concrete.ml.sklearn import LogisticRegression, LinearSVC, RandomForestClassifier

train_df = pd.read_csv("/Users/mariaasoltanei/Desktop/FACULTATE/CERCETARE/HealthApp/ML/TestDataProcesing/CSVs/train.csv")
test_df = pd.read_csv("/Users/mariaasoltanei/Desktop/FACULTATE/CERCETARE/HealthApp/ML/TestDataProcesing/CSVs/test.csv")

# Define activity label mapping
activity_map = {
    "WALKING": 1,
    "WALKING_UPSTAIRS": 2,
    "WALKING_DOWNSTAIRS": 3,
    "SITTING": 4,
    "STANDING": 5,
    "LAYING": 6
}

# Apply the mapping to the training data
train_df["Activity"] = train_df["ActivityName"].map(activity_map)

X_train = train_df.drop(columns=["Activity", "ActivityName"])
y_train = train_df["Activity"]

X_test = test_df.copy()
models = {
    "LogisticRegression": LogisticRegression(n_bits=7),
    "LinearSVC": LinearSVC(n_bits=7),
}

# Evaluate each model
for name, model in models.items():
    print(f"\n🔍 Testing model: {name}")

    model.fit(X_train, y_train)
    y_pred_clear = model.predict(X_test)

    try:
        model.compile(X_train)
        y_pred_fhe = model.predict(X_test, fhe="execute")
        similarity = (y_pred_fhe == y_pred_clear).mean() * 100
        print(f"In clear : {y_pred_clear}")
        print(f"In FHE   : {y_pred_fhe}")
        print(f"Similarity: {similarity:.2f}%")
    except Exception as e:
        print(f" FHE not supported for {name}: {e}")
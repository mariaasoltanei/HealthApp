import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# 1. Load training data
train_df = pd.read_csv("/Users/mariaasoltanei/Desktop/FACULTATE/CERCETARE/HealthApp/Backend/Data/DataProcessing/train_features.csv")
X_train = train_df.drop(columns=["Activity"])
y_train = train_df["Activity"]

# 2. Fit scaler on training data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)

# 3. Train Random Forest on scaled data
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# 4. Load your phone's test data
test_df = pd.read_csv("/Users/mariaasoltanei/Desktop/FACULTATE/CERCETARE/HealthApp/Backend/Data/MockData/merged.csv")

# 5. Apply the SAME scaler to the phone test data
test_scaled = scaler.transform(test_df)

# 6. Predict activities
predictions = model.predict(test_scaled)

# 7. Output predictions
print("Predicted activity labels after scaling:")
for i, label in enumerate(predictions):
    print(f"Sample {i}: Activity {label}")

import pandas as pd
import joblib
from concrete.ml.sklearn import LinearSVC

df = pd.read_csv("/Users/mariaasoltanei/Desktop/FACULTATE/CERCETARE/HealthApp/ML/TestDataProcesing/CSVs/train.csv")

activity_map = {
    "WALKING": 1,
    "WALKING_UPSTAIRS": 2,
    "WALKING_DOWNSTAIRS": 3,
    "SITTING": 4,
    "STANDING": 5,
    "LAYING": 6
}

# Apply the mapping to the training data
df["Activity"] = df["ActivityName"].map(activity_map)

X = df.drop(columns=["Activity", "ActivityName"])
# Save a sample input for FHE model compilation later
sample_input = X.iloc[[0]].values
import numpy as np
np.save("sample_input.npy", sample_input)

y = df["Activity"]

model = LinearSVC(n_bits=7)
model.fit(X, y)
# model.compile(X)

joblib.dump(model, "lsvc_concrete_model.pkl")
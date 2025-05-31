import pandas as pd
import joblib
from concrete.ml.sklearn import LinearSVC, XGBClassifier
from concrete.ml.deployment import FHEModelClient, FHEModelDev, FHEModelServer

df = pd.read_csv("/Users/mariaasoltanei/Desktop/FACULTATE/CERCETARE/HealthApp/ML/TestDataProcesing/CSVs/train.csv")

activity_map = {
    "WALKING": 1,
    "WALKING_UPSTAIRS": 2,
    "WALKING_DOWNSTAIRS": 3,
    "SITTING": 4,
    "STANDING": 5,
    "LAYING": 6
}

df["Activity"] = df["ActivityName"].map(activity_map)

X = df.drop(columns=["Activity", "ActivityName"])
print(X.columns)

from sklearn.preprocessing import LabelEncoder
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df["Activity"])
import numpy as np
np.save("label_classes.npy", label_encoder.classes_)
print(y)

model = model = XGBClassifier(n_bits=7)
model.fit(X, y)
model.compile(X)

fhemodel_dev = FHEModelDev("/Users/mariaasoltanei/Desktop/FACULTATE/CERCETARE/HealthApp/ML/HETest/Model", model)
fhemodel_dev.save()

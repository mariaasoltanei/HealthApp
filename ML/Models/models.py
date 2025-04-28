import pandas as pd
import os
from concrete.ml.sklearn import LinearRegression, LogisticRegression, NeuralNetClassifier, RandomForestClassifier, DecisionTreeClassifier, LinearSVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import make_pipeline
from torch import nn
notebook_dir = os.getcwd()
data_dir = os.path.abspath(os.path.join(notebook_dir, "ML"))


train_df = pd.read_csv(data_dir+"/UCIProcessing/CSVs/train_with_freq.csv")
test_df = pd.read_csv(data_dir+"/TestDataProcesing/CSVs/test_with_freq.csv")

# Drop labels from test set (no Activity/ActivityName there)
X_test = test_df.copy()

# Extract features and labels from train set
X_train = train_df.drop(columns=["Activity", "ActivityName"])
y_train = train_df["Activity"]

# Match test data features exactly
X_test = test_df[X_train.columns]  # force same column order and selection

# Normalize
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

params = {
    "module__n_layers": 2,
    "module__n_w_bits": 4,
    "module__n_a_bits": 4,
    "module__n_hidden_neurons_multiplier": 0.5,
    "module__activation_function": nn.ReLU,
    "max_epochs": 7,
}
models = {
    "Neural Network": NeuralNetClassifier(**params),
    "Logistic Regression": LogisticRegression(n_bits=6),
    "Random Forest": RandomForestClassifier(n_bits=6, n_estimators=10),
    "Linear SVC": LinearSVC(n_bits=6, C=0.1),
}

activity_labels = {
    1: "WALKING",
    2: "WALKING_UPSTAIRS",
    3: "WALKING_DOWNSTAIRS",
    4: "SITTING",
    5: "STANDING",
    6: "LAYING"
}

#truth:  LAYING WALKING SITTING STANDING

for name, model in models.items():
    print(f"\n🧠 Training: {name}")
    model.fit(X_train_scaled, y_train)
    model.compile(X_train_scaled)
    
    print("🔐 Simulating encrypted inference...")
    y_pred = model.predict(X_test_scaled, fhe="simulate")
    print()
    pred_names = [activity_labels.get(int(pred), "UNKNOWN") for pred in y_pred]


    print(pred_names)

import numpy as np
import pandas as pd
import os


data_dir = "Backend/Data/uci_har_dataset/train/Inertial Signals"

# === FEATURE EXTRACTION ===
def extract_features(windows, prefix):
    return pd.DataFrame({
        f"{prefix}_mean": np.mean(windows, axis=1),
        f"{prefix}_std": np.std(windows, axis=1),
        f"{prefix}_max": np.max(windows, axis=1),
        f"{prefix}_min": np.min(windows, axis=1),
        f"{prefix}_energy": np.mean(np.square(windows), axis=1),
        f"{prefix}_iqr": np.percentile(windows, 75, axis=1) - np.percentile(windows, 25, axis=1),
        f"{prefix}_sma": np.sum(np.abs(windows), axis=1) / windows.shape[1],
        f"{prefix}_mad": np.mean(np.abs(windows - np.mean(windows, axis=1, keepdims=True)), axis=1),
        f"{prefix}_amplitude": np.max(windows, axis=1) - np.min(windows, axis=1),
    })

# === LOAD AND PROCESS ALL SIGNALS ===
def process_inertial_signals():
    signals = {
        "body_acc": ["x", "y", "z"],
        "body_gyro": ["x", "y", "z"],
        "total_acc": ["x", "y", "z"],
    }
    
    all_features = []

    for sensor, axes in signals.items():
        for axis in axes:
            file_name = f"{sensor}_{axis}_train.txt"
            file_path = os.path.join(data_dir, file_name)
            print(f"Loading {file_name}...")
            signal = np.loadtxt(file_path)
            features = extract_features(signal, f"{sensor}_{axis}")
            all_features.append(features)

    # Combine all features into one DataFrame
    return pd.concat(all_features, axis=1)

def load_activity_labels():
    label_path = os.path.join(data_dir, "y_train.txt")
    print("Loading activity labels...")
    return pd.read_csv(label_path, header=None, names=["activity"])

# === RUN ===
train_df = process_inertial_signals()
activity_labels = load_activity_labels()

# Attach labels to the features
train_df["Activity"] = activity_labels
train_df.to_csv("train_features.csv", index=False)
print("Saved to train_features.csv")
print(train_df.shape)
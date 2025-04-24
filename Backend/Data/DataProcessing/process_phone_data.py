import pandas as pd
import numpy as np
import os

# === CONFIG ===
# Set this to your CSV path
csv_path = "/Users/mariaasoltanei/Desktop/FACULTATE/CERCETARE/HealthApp/Backend/Data/DataProcessing/mockDataOriginal.csv"
output_csv = "test_features.csv"

# === LOAD DATA ===
df = pd.read_csv(csv_path)
accel = df[df['sensor_type'] == 'accelerometer'].sort_values(by='timestamp').reset_index(drop=True)
gyro = df[df['sensor_type'] == 'gyroscope'].sort_values(by='timestamp').reset_index(drop=True)

# === WINDOWING FUNCTION (50% OVERLAP) ===
def create_overlapping_windows(df, window_size=128, stride=64):
    values = df[['x', 'y', 'z']].values
    windows = []
    for start in range(0, len(values) - window_size + 1, stride):
        windows.append(values[start:start + window_size])
    return np.array(windows)

accel_windows = create_overlapping_windows(accel)
gyro_windows = create_overlapping_windows(gyro)
min_len = min(len(accel_windows), len(gyro_windows))
accel_windows = accel_windows[:min_len]
gyro_windows = gyro_windows[:min_len]

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

def extract_features_by_axis(windows, label_prefix):
    dfs = []
    for i, axis in enumerate(['x', 'y', 'z']):
        dfs.append(extract_features(windows[:, :, i], f"{label_prefix}_{axis}"))
    return pd.concat(dfs, axis=1)

# === BUILD FEATURE DATAFRAME ===
accel_df = extract_features_by_axis(accel_windows, "body_acc")
gyro_df = extract_features_by_axis(gyro_windows, "body_gyro")
accel_df.dropna(inplace=True)
gyro_df.dropna(inplace=True)
total_acc_df = pd.DataFrame(0, index=range(min_len), columns=[
    f"total_acc_{axis}_{stat}" for axis in ['x', 'y', 'z']
    for stat in ['mean', 'std', 'max', 'min', 'energy', 'iqr', 'sma', 'mad', 'amplitude']
])

final_df = pd.concat([accel_df, gyro_df, total_acc_df], axis=1)
final_df.to_csv(output_csv, index=False)
print(f"✅ Saved to {output_csv}")

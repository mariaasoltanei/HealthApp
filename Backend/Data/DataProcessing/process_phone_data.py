import pandas as pd
import numpy as np
import os
from scipy.signal import butter, filtfilt, medfilt

# === CONFIG ===
INPUT_CSV = "/Users/mariaasoltanei/Desktop/FACULTATE/CERCETARE/HealthApp/Backend/Data/DataProcessing/mockDataPhone1.csv"
OUTPUT_CSV = "/Users/mariaasoltanei/Desktop/FACULTATE/CERCETARE/HealthApp/Backend/Data/DataProcessing/test_features.csv"
WINDOW_SIZE = 128
STRIDE = 64
FS = 50  # Sampling rate (Hz)

# === FILTER HELPERS ===
def butter_lowpass_filter(data, cutoff, fs, order=3):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, data)

def apply_filter(signal, fs=50, median_kernel=3, lpf_cutoff=20):
    signal = medfilt(signal, kernel_size=median_kernel)
    return butter_lowpass_filter(signal, lpf_cutoff, fs)

# === FEATURE EXTRACTION ===
def extract_stats(signal, prefix):
    return {
        f"{prefix}_mean": np.mean(signal),
        f"{prefix}_std": np.std(signal),
        f"{prefix}_max": np.max(signal),
        f"{prefix}_min": np.min(signal),
        f"{prefix}_energy": np.mean(np.square(signal)),
        f"{prefix}_iqr": np.percentile(signal, 75) - np.percentile(signal, 25),
        f"{prefix}_sma": np.sum(np.abs(signal)) / len(signal),
        f"{prefix}_mad": np.mean(np.abs(signal - np.mean(signal))),
        f"{prefix}_amplitude": np.max(signal) - np.min(signal)
    }

def extract_window_features(df_window):
    features = {}
    for sensor in ['body_acc', 'body_gyro', 'total_acc']:
        for axis in ['x', 'y', 'z']:
            col_name = f"{sensor}_{axis}"
            if col_name in df_window.columns:
                stats = extract_stats(df_window[col_name].values, col_name)
            else:
                stats = extract_stats(np.zeros(len(df_window)), col_name)
            features.update(stats)
    return features

# === LOAD AND PREPROCESS ===
df = pd.read_csv(INPUT_CSV)
df = df[df['sensor_type'].isin(['accelerometer', 'gyroscope'])]
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
df.set_index('timestamp', inplace=True)
df = df.groupby('sensor_type').resample('20ms').mean().drop(columns='user_id').dropna().reset_index()

# === PROCESS EACH SENSOR ===
processed = []

for sensor in ['accelerometer', 'gyroscope']:
    sensor_df = df[df['sensor_type'] == sensor].sort_values('timestamp').reset_index(drop=True)

    for axis in ['x', 'y', 'z']:
        filtered = apply_filter(sensor_df[axis].values, fs=FS)
        sensor_df[f"{axis}_filtered"] = filtered

        if sensor == 'accelerometer':
            gravity = butter_lowpass_filter(filtered, cutoff=0.3, fs=FS)
            body = filtered - gravity
            jerk = np.gradient(body, 1/FS)

            sensor_df[f"{axis}_gravity"] = gravity
            sensor_df[f"{axis}_body"] = body
            sensor_df[f"{axis}_jerk"] = jerk

    if sensor == 'accelerometer':
        sensor_df['body_acc_mag'] = np.sqrt(
            sensor_df['x_body']**2 + sensor_df['y_body']**2 + sensor_df['z_body']**2
        )
        sensor_df['body_jerk_mag'] = np.sqrt(
            sensor_df['x_jerk']**2 + sensor_df['y_jerk']**2 + sensor_df['z_jerk']**2
        )

    if sensor == 'gyroscope':
        sensor_df['gyro_mag'] = np.sqrt(
            sensor_df['x_filtered']**2 + sensor_df['y_filtered']**2 + sensor_df['z_filtered']**2
        )

    processed.append(sensor_df)

# === MERGE ACCEL + GYRO ===
merged = pd.merge_asof(
    processed[0].sort_values('timestamp'),
    processed[1].sort_values('timestamp'),
    on='timestamp',
    direction='nearest',
    suffixes=('_accel', '_gyro')
)

# === RENAME TO UCI-COMPATIBLE NAMES ===
renamed_df = pd.DataFrame({
    'body_acc_x': merged['x_body'],
    'body_acc_y': merged['y_body'],
    'body_acc_z': merged['z_body'],
    'total_acc_x': merged['x_filtered_accel'],  # ← corrected!
    'total_acc_y': merged['y_filtered_accel'],
    'total_acc_z': merged['z_filtered_accel'],
    'body_gyro_x': merged['x_filtered_gyro'],
    'body_gyro_y': merged['y_filtered_gyro'],
    'body_gyro_z': merged['z_filtered_gyro'],
})

# === SLIDE WINDOWS AND EXTRACT FEATURES ===
features = []
for start in range(0, len(renamed_df) - WINDOW_SIZE + 1, STRIDE):
    window = renamed_df.iloc[start:start + WINDOW_SIZE]
    feature_row = extract_window_features(window)
    features.append(feature_row)

# === FINAL OUTPUT ===
feature_df = pd.DataFrame(features)
feature_df.to_csv(OUTPUT_CSV, index=False)
print(f"✅ Final test features (UCI HAR-style) saved to {OUTPUT_CSV}")
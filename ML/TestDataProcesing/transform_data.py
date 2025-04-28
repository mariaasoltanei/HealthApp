import os
import numpy as np
import pandas as pd
from scipy.stats import entropy

notebook_dir = os.getcwd()
data_dir = os.path.abspath(os.path.join(notebook_dir, "ML"))

# --- CONFIG ---
WINDOW_SIZE = 128
OVERLAP = 0.5
SAMPLING_RATE = 50
RAW_TEST_FILE = data_dir+"/TestDataProcesing/CSVs/mockDataPhone.csv"
OUTPUT_FILE = data_dir+"/TestDataProcesing/CSVs/test_with_freq.csv"

# --- TIME-DOMAIN FEATURE FUNCTIONS ---
def findEnergy(arr):
    return np.sum(np.square(arr)) / len(arr)

def findQuantile(arr):
    return np.percentile(arr, 75) - np.percentile(arr, 25)

def findSMA(arr):
    return np.sum(np.abs(arr)) / len(arr)

def findMad(arr):
    return np.median(np.abs(arr - np.median(arr)))

def findAmplitude(arr):
    return max(arr) - min(arr)

# --- FREQUENCY-DOMAIN FEATURE FUNCTIONS ---
def findFreqFeatures(arr, sampling_rate=50):
    fft_vals = np.abs(np.fft.rfft(arr))
    fft_freqs = np.fft.rfftfreq(len(arr), d=1/sampling_rate)

    power_spectrum = fft_vals**2
    total_power = np.sum(power_spectrum)

    ps_norm = power_spectrum / total_power if total_power > 0 else power_spectrum

    return {
        'dominant_freq': fft_freqs[np.argmax(fft_vals)],
        'mean_freq': np.sum(fft_freqs * ps_norm) if total_power > 0 else 0,
        'freq_energy': np.sum(power_spectrum),
        'entropy': entropy(ps_norm) if total_power > 0 else 0
    }

# --- WINDOWING ---
def create_overlapping_windows(df, window_size=128, overlap=0.5):
    step = int(window_size * (1 - overlap))
    windows = []
    for start in range(0, len(df) - window_size + 1, step):
        window = df.iloc[start:start+window_size][['x', 'y', 'z']].to_numpy()
        windows.append(window)
    return windows

# --- FEATURE EXTRACTION FOR A SENSOR ---
def extract_features_from_window(window, sensor_prefix):
    row = {}
    for i, axis in enumerate(['x', 'y', 'z']):
        axis_data = window[:, i]
        # Time-domain features
        row.update({
            f"{sensor_prefix}_{axis}_mean": np.mean(axis_data),
            f"{sensor_prefix}_{axis}_std": np.std(axis_data),
            f"{sensor_prefix}_{axis}_max": np.max(axis_data),
            f"{sensor_prefix}_{axis}_min": np.min(axis_data),
            f"{sensor_prefix}_{axis}_energy": findEnergy(axis_data),
            f"{sensor_prefix}_{axis}_iqr": findQuantile(axis_data),
            f"{sensor_prefix}_{axis}_sma": findSMA(axis_data),
            f"{sensor_prefix}_{axis}_mad": findMad(axis_data),
            f"{sensor_prefix}_{axis}_amplitude": findAmplitude(axis_data),
        })
        # Frequency-domain features
        freq_feats = findFreqFeatures(axis_data)
        for k, v in freq_feats.items():
            row[f"{sensor_prefix}_{axis}_{k}"] = v
    return row

# --- PROCESS RAW SENSOR DATA ---
def process_sensor_data(sensor_df, sensor_type):
    windows = create_overlapping_windows(sensor_df, WINDOW_SIZE, OVERLAP)
    return pd.DataFrame([extract_features_from_window(w, sensor_type) for w in windows])

# --- MAIN PROCESSING FUNCTION ---
def prepare_test_data(raw_csv=RAW_TEST_FILE, output_csv=OUTPUT_FILE):
    df = pd.read_csv(raw_csv)

    acc_df = df[df['sensor_type'] == 'accelerometer'].reset_index(drop=True)
    gyro_df = df[df['sensor_type'] == 'gyroscope'].reset_index(drop=True)

    df_accel_features = process_sensor_data(acc_df, "total_acc")
    df_gyro_features = process_sensor_data(gyro_df, "body_gyro")

    min_len = min(len(df_accel_features), len(df_gyro_features))
    df_combined = pd.concat([
        df_accel_features.iloc[:min_len].reset_index(drop=True),
        df_gyro_features.iloc[:min_len].reset_index(drop=True)
    ], axis=1)

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df_combined.to_csv(output_csv, index=False)
    print(f"Test data processed and saved to: {output_csv}")
    return df_combined

# --- Run it ---
if __name__ == "__main__":
    prepare_test_data()

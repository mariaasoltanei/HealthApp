import os
import numpy as np
import pandas as pd
from scipy.stats import entropy

notebook_dir = os.getcwd()
data_dir = os.path.abspath(os.path.join(notebook_dir, "ML"))

# --- Helper functions (time-domain) ---
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

# --- Helper functions (frequency-domain) ---
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

def prepareDataFrame(df_type, base_path=data_dir+"/uci_har_dataset"):
    axes = ['x', 'y', 'z']
    sensors = ['body_gyro', 'total_acc']
    time_features = ['mean', 'std', 'max', 'min', 'energy', 'iqr', 'sma', 'mad', 'amplitude']
    freq_features = ['dominant_freq', 'mean_freq', 'freq_energy', 'entropy']

    # Initialize dictionary
    data_dict = {
        f"{sensor}_{axis}_{feature}": []
        for sensor in sensors
        for axis in axes
        for feature in time_features + freq_features
    }

    # Collect file paths
    file_paths = [
        os.path.join(base_path, df_type, "Inertial Signals", f"{sensor}_{axis}_{df_type}.txt")
        for sensor in sensors
        for axis in axes
    ]

    for file_path in file_paths:
        filename = os.path.basename(file_path)
        parts = filename.split('_')[:3]
        column_name = '_'.join(parts)  # e.g., total_acc_x

        with open(file_path) as f:
            lines = f.readlines()

        for line in lines:
            window = line.replace('  ', ' ').strip().split()
            floats = np.array([float(x) for x in window])

            # Time-domain features
            data_dict[f"{column_name}_mean"].append(np.mean(floats))
            data_dict[f"{column_name}_std"].append(np.std(floats))
            data_dict[f"{column_name}_max"].append(np.max(floats))
            data_dict[f"{column_name}_min"].append(np.min(floats))
            data_dict[f"{column_name}_energy"].append(findEnergy(floats))
            data_dict[f"{column_name}_iqr"].append(findQuantile(floats))
            data_dict[f"{column_name}_sma"].append(findSMA(floats))
            data_dict[f"{column_name}_mad"].append(findMad(floats))
            data_dict[f"{column_name}_amplitude"].append(findAmplitude(floats))

            # Frequency-domain features
            freq_dict = findFreqFeatures(floats)
            for feature_name, val in freq_dict.items():
                data_dict[f"{column_name}_{feature_name}"].append(val)

    return pd.DataFrame(data_dict)

# Activity label mapping
def load_label_mapping(path):
    mapping = {}
    with open(path) as f:
        for line in f.readlines():
            k, v = line.strip().split()
            mapping[int(k)] = v
    return mapping

# Main
if __name__ == "__main__":
    label_mapping = load_label_mapping(data_dir + '/uci_har_dataset/activity_labels.txt')

    df_train = prepareDataFrame("train")
    y_train = pd.read_csv(data_dir + '/uci_har_dataset/train/y_train.txt', header=None)

    df_train['Activity'] = y_train
    df_train['ActivityName'] = df_train['Activity'].map(label_mapping)

    output_path = os.path.join(data_dir, 'UCIProcessing/CSVs/train_with_freq.csv')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_train.to_csv(output_path, index=False)
    print(f"Saved updated training data with frequency features to: {output_path}")

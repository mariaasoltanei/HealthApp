
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
RAW_TEST_FILE = data_dir+"/TestDataProcesing/CSVs/labeledMockDataPhone.csv"
OUTPUT_FILE = data_dir+"/TestDataProcesing/CSVs/train_with_freq.csv"

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

    if total_power == 0:
        normalized_power = np.zeros_like(power_spectrum)
    else:
        normalized_power = power_spectrum / total_power

    spectral_entropy = entropy(normalized_power)
    dominant_frequency = fft_freqs[np.argmax(power_spectrum)]
    spectral_energy = np.sum(power_spectrum) / len(power_spectrum)

    return spectral_entropy, dominant_frequency, spectral_energy

# --- MAIN PROCESSING ---
def process_data():
    df = pd.read_csv(RAW_TEST_FILE)

    # Sort by timestamp
    df = df.sort_values(by="timestamp").reset_index(drop=True)

    step_size = int(WINDOW_SIZE * (1 - OVERLAP))
    features_list = []

    for start in range(0, len(df) - WINDOW_SIZE + 1, step_size):
        end = start + WINDOW_SIZE
        window = df.iloc[start:end]

        if len(window) == WINDOW_SIZE:
            feature_dict = {}

            for axis in ['x', 'y', 'z']:
                axis_data = window[axis]

                # Time-domain features
                feature_dict[f'{axis}_mean'] = axis_data.mean()
                feature_dict[f'{axis}_std'] = axis_data.std()
                feature_dict[f'{axis}_energy'] = findEnergy(axis_data)
                feature_dict[f'{axis}_quantile'] = findQuantile(axis_data)
                feature_dict[f'{axis}_sma'] = findSMA(axis_data)
                feature_dict[f'{axis}_mad'] = findMad(axis_data)
                feature_dict[f'{axis}_amplitude'] = findAmplitude(axis_data)

                # Frequency-domain features
                spectral_entropy, dominant_frequency, spectral_energy = findFreqFeatures(axis_data, sampling_rate=SAMPLING_RATE)
                feature_dict[f'{axis}_spectral_entropy'] = spectral_entropy
                feature_dict[f'{axis}_dominant_frequency'] = dominant_frequency
                feature_dict[f'{axis}_spectral_energy'] = spectral_energy

            # Assign the most frequent Activity label in the window
            activity_label = window['Activity'].mode()[0]  # If you want ActivityName, use 'ActivityName' instead
            feature_dict['Activity'] = activity_label

            features_list.append(feature_dict)

    features_df = pd.DataFrame(features_list)
    features_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Feature extraction completed! Output saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    process_data()

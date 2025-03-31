import pymongo
import pandas as pd
import numpy as np
import math
import statsmodels.api as sm
from scipy.signal import butter, filtfilt, medfilt
from scipy.stats import median_abs_deviation, entropy
from scipy.fft import fft
from scipy.stats import pearsonr

def applyFilters(df):
    fs = 50 
    f_cutoff = 20  
    f_cutoff2 = 0.3  # Second filter cutoff frequency (Hz)
    df = medfilt(df, kernel_size=5)  #kernel_size=2

    b, a = butter(3, f_cutoff/(fs/2), 'low')
    df_filtered = filtfilt(b, a, df, axis=0)

    b2, a2 = butter(3, f_cutoff2/(fs/2), 'low')
    gravity = filtfilt(b2, a2, df_filtered, axis=0)

    return df_filtered, gravity

def filterAcceleration(df):
    df_filtered, gravity = applyFilters(df)
    body = df_filtered - gravity
    return body

def filterGravity(df):
    df_filtered, gravity = applyFilters(df)
    return gravity

def findBodyJerk(dfAccData):
    dt = pd.to_datetime(dfAccData['timestamp']).diff().apply(lambda x: x/np.timedelta64(1, 'ms')).fillna(0).astype('int64')

    vx = dfAccData['xBody'].diff() / dt
    vy = dfAccData['yBody'].diff() / dt
    vz = dfAccData['zBody'].diff() / dt

    jx = vx.diff() / dt
    jy = vy.diff() / dt
    jz = vz.diff() / dt

    return vx, vy, vz

def findSMA(signal):
    sma = sum(abs(value) for value in signal)
    return sma

def findAmplitude(signal):
    np_fft = np.fft.fft(signal)
    amplitudes = 2 / 128 * np.abs(np_fft) 
    return amplitudes.mean()

def findMad(data):
    median = np.median(data)
    deviations = np.abs(data - median)
    mad = np.median(deviations)
    return mad

def findSMAMagnitude(df):
    sum_abs = np.abs(df)
    return (sum_abs/len(df)).mean()

def findEnergy(signal):
    return sum(x ** 2 for x in signal)
    #Sum of the squares divided by the number of values. 

def findQuantile(data):
    sorted_data = sorted(data)
    n = len(sorted_data)
    
    q1_index = int(0.25 * (n + 1))  # Index of the first quartile
    q3_index = int(0.75 * (n + 1))  # Index of the third quartile
    
    q1 = sorted_data[q1_index]
    q3 = sorted_data[q3_index]
    
    iqr = q3 - q1
    return iqr

def findCorrelation(signal1, signal2):
    correlation, _ = pearsonr(signal1, signal2)
    return correlation
def findEntropy(data):
    frequency = {}
    n = len(data)

    # Count the occurrences of each unique value
    for value in data:
        if value in frequency:
            frequency[value] += 1
        else:
            frequency[value] = 1

    entropy = 0.0
    for count in frequency.values():
        probability = count / n
        entropy -= probability * math.log2(probability)

    return entropy


def entropy1(labels, base=None):
  value,counts = np.unique(labels, return_counts=True)
  return entropy(counts, base=base)


def findArCoeff(df, order):
    rho, sigma2 = sm.regression.linear_model.burg(df, order=order)
    return rho

def findMagnitudeBody(df):
    return np.sqrt(df['xBody']**2 + df['yBody']**2 + df['zBody']**2)

def findMagnitudeGravity(df):
    return np.sqrt(df['xGravity']**2 + df['yGravity']**2 + df['zGravity']**2)

def findMagnitudeBodyJerk(df):
    return np.sqrt(df['xBodyJerk']**2 + df['yBodyJerk']**2 + df['zBodyJerk']**2)

def findFFT(df):
    return np.abs(np.fft.fft(df.values))
     
def maxInds(df):
    max_index = np.argmax(np.abs(df))
    return max_index
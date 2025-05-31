import sys
import os
import pandas as pd
from collections import Counter

notebook_dir = os.getcwd()
data_dir = os.path.abspath(os.path.join(notebook_dir, ".."))
sys.path.append(data_dir+"/HealthApp/ML")
from processingFunctions import *

csv_path = os.path.join(os.getcwd(), "/Users/mariaasoltanei/Desktop/FACULTATE/CERCETARE/HealthApp/ML/TestDataProcesing/CSVs/labeledMockDataPhone.csv")

df = pd.read_csv(csv_path)

sensor_groups = {sensor: data for sensor, data in df.groupby('sensor_type')}
dfGyroData = sensor_groups.get('gyroscope')
dfAccData = sensor_groups.get('accelerometer')

dfGyroData = dfGyroData.sort_values('timestamp')
dfAccData = dfAccData.sort_values('timestamp')
dfAccData['timestamp'] = pd.to_datetime(dfAccData['timestamp'], unit='ms')
dfGyroData['timestamp'] = pd.to_datetime(dfGyroData['timestamp'], unit='ms')

dfGyroData.drop(columns=['sensor_type', 'user_id'], inplace=True)
dfAccData.drop(columns=['sensor_type', 'user_id'], inplace=True)

#xBody is body_acc, x is total_acc
dfAccData['xAccBody'] = filterAcceleration(dfAccData['x'])
dfAccData['yAccBody'] = filterAcceleration(dfAccData['y'])
dfAccData['zAccBody'] = filterAcceleration(dfAccData['z'])

dfGyroData['xGyroBody'] = filterAcceleration(dfGyroData['x'])
dfGyroData['yGyroBody'] = filterAcceleration(dfGyroData['y'])
dfGyroData['zGyroBody'] = filterAcceleration(dfGyroData['z'])

dfGyroData.drop(columns=['x', 'y', 'z'], inplace=True)
dfAccData.rename(columns={'x': 'xAccTotal', 'y': 'yAccTotal', 'z': 'zAccTotal'}, inplace=True)
# dfGyroData.rename(columns={'xGyroBody': 'x', 'yGyroBody': 'y', 'zGyroBody': 'z'}, inplace=True)

merged_df = pd.merge_asof(dfAccData, dfGyroData, on=['timestamp'], tolerance=pd.Timedelta('150ms'))
merged_df.dropna(inplace=True)
merged_df.drop(columns=['Activity_x', 'ActivityName_x'], inplace=True)
merged_df.rename(columns={'Activity_y': 'Activity', 'ActivityName_y': 'ActivityName'}, inplace=True)

testDataDict = {
        'body_acc_x_mean': [],
        'body_acc_y_mean': [],
        'body_acc_z_mean': [],
        'body_acc_x_std': [],
        'body_acc_y_std': [],
        'body_acc_z_std': [],
        'body_acc_x_max': [],
        'body_acc_y_max': [],
        'body_acc_z_max': [],
        'body_acc_x_min': [],
        'body_acc_y_min': [],
        'body_acc_z_min': [],
        'body_acc_x_energy': [],
        'body_acc_y_energy': [],
        'body_acc_z_energy': [],
        'body_acc_x_iqr': [],
        'body_acc_y_iqr': [],
        'body_acc_z_iqr': [],
        'body_acc_x_sma': [],
        'body_acc_y_sma': [],
        'body_acc_z_sma': [],
        'body_acc_x_mad': [],
        'body_acc_y_mad': [],
        'body_acc_z_mad': [],
        'body_acc_x_amplitude': [],
        'body_acc_y_amplitude': [],
        'body_acc_z_amplitude': [],

        'body_gyro_x_mean': [],
        'body_gyro_y_mean': [],
        'body_gyro_z_mean': [],
        'body_gyro_x_std': [],
        'body_gyro_y_std': [],
        'body_gyro_z_std': [],
        'body_gyro_x_max': [],
        'body_gyro_y_max': [],
        'body_gyro_z_max': [],
        'body_gyro_x_min': [],
        'body_gyro_y_min': [],
        'body_gyro_z_min': [],
        'body_gyro_x_energy': [],
        'body_gyro_y_energy': [],
        'body_gyro_z_energy': [],
        'body_gyro_x_iqr': [],
        'body_gyro_y_iqr': [],
        'body_gyro_z_iqr': [],
        'body_gyro_x_sma': [],
        'body_gyro_y_sma': [],
        'body_gyro_z_sma': [],
        'body_gyro_x_mad': [],
        'body_gyro_y_mad': [],
        'body_gyro_z_mad': [],
        'body_gyro_x_amplitude': [],
        'body_gyro_y_amplitude': [],
        'body_gyro_z_amplitude': [],

        'total_acc_x_mean': [],
        'total_acc_y_mean': [],
        'total_acc_z_mean': [],
        'total_acc_x_std': [],
        'total_acc_y_std': [],
        'total_acc_z_std': [],
        'total_acc_x_max': [],
        'total_acc_y_max': [],
        'total_acc_z_max': [],
        'total_acc_x_min': [],
        'total_acc_y_min': [],
        'total_acc_z_min': [],
        'total_acc_x_energy': [],
        'total_acc_y_energy': [],
        'total_acc_z_energy': [],
        'total_acc_x_iqr': [],
        'total_acc_y_iqr': [],
        'total_acc_z_iqr': [],
        'total_acc_x_sma': [],
        'total_acc_y_sma': [],
        'total_acc_z_sma': [],
        'total_acc_x_mad': [],
        'total_acc_y_mad': [],
        'total_acc_z_mad': [],
        'total_acc_x_amplitude': [],
        'total_acc_y_amplitude': [],
        'total_acc_z_amplitude': [],
        'Activity': [],
        'ActivityName': [],
}
window_length = 128
overlap_pct = 0.5
shift = int(window_length * overlap_pct)
# colNames = ['body_acc_x','body_acc_y','body_acc_z', 'body_gyro_x', 'body_gyro_y', 'body_gyro_z', 'total_acc_x', 'total_acc_y', 'total_acc_z']
colNames = {
    'body_acc_x': 'xAccBody',
    'body_acc_y': 'yAccBody',
    'body_acc_z':'zAccBody',
    'body_gyro_x': 'xGyroBody',
    'body_gyro_y': 'yGyroBody',
    'body_gyro_z': 'zGyroBody',
    'total_acc_x': 'xAccTotal',
    'total_acc_y': 'yAccTotal',
    'total_acc_z': 'zAccTotal'
}

windowed_data = []
windowNo = 1
#raport activitate pe zi
for i in range(0, len(merged_df) - window_length, shift):
    window = merged_df.iloc[i:i+window_length]

    if len(window) < window_length:
        continue

    print(windowNo, ': ', (window['timestamp'].values[0]),'---->' ,window['timestamp'].values[-1],'\n')
    windowNo = windowNo +1
    for name in colNames:
        if("total" in name):
            testDataDict[name +"_mean"].append(np.mean(window[colNames[name]]))
            testDataDict[name +"_std"].append(np.std(window[colNames[name]]))
            testDataDict[name +"_max"].append(max(window[colNames[name]]))
            testDataDict[name +"_min"].append(min(window[colNames[name]]))
            testDataDict[name + "_energy"].append(findEnergy(window[colNames[name]].values))
            testDataDict[name + "_iqr"].append(findQuantile(window[colNames[name]].values))
            testDataDict[name + "_sma"].append(findSMA(window[colNames[name]].values))
            testDataDict[name + "_mad"].append(findMad(window[colNames[name]].values))
            testDataDict[name + "_amplitude"].append(findAmplitude(window[colNames[name]].values))
        else:
            testDataDict[name +"_mean"].append(np.mean(window[colNames[name]]))
            testDataDict[name +"_std"].append(np.std(window[colNames[name]]))
            testDataDict[name +"_max"].append(max(window[colNames[name]]))
            testDataDict[name +"_min"].append(min(window[colNames[name]]))
            testDataDict[name + "_energy"].append(findEnergy(window[colNames[name]].values))
            testDataDict[name + "_iqr"].append(findQuantile(window[colNames[name]].values))
            testDataDict[name + "_sma"].append(findSMA(window[colNames[name]].values))
            testDataDict[name + "_mad"].append(findMad(window[colNames[name]].values))
            testDataDict[name + "_amplitude"].append(findAmplitude(window[colNames[name]].values))
    # Add activity and activity name
    common_activity = Counter(window['Activity']).most_common(1)
    print("Window activity distribution:", window['ActivityName'].value_counts())
    activity_counts = window['ActivityName'].value_counts(normalize=True)
    if activity_counts.iloc[0] >= 0.7:
        label = activity_counts.index[0]
    else:
        label = 'UNKNOWN'


    testDataDict['Activity'].append(window['Activity'].mode()[0])
    testDataDict['ActivityName'].append(window['ActivityName'].mode()[0])

testDataDF = pd.DataFrame(testDataDict)
testDataDF.to_csv(data_dir + "/HealthApp/ML/TestDataProcesing/CSVs/train.csv", encoding='utf-8', index=False)

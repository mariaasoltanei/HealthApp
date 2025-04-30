from processingFunctions import *
from testDataDict import testDataDict
import pandas as pd
import numpy as np
from collections import Counter

def get_merged_dataframe(accelerometer_data: pd.DataFrame, gyroscope_data: pd.DataFrame) -> pd.DataFrame:
    gyroscope_data = gyroscope_data.sort_values('Time')
    accelerometer_data = accelerometer_data.sort_values('Time')
    gyroscope_data.rename(columns={'root.users.user_1.gyroscope.x': 'x', 'root.users.user_1.gyroscope.y': 'y', 'root.users.user_1.gyroscope.z': 'z'}, inplace=True)
    accelerometer_data.rename(columns={'root.users.user_1.accelerometer.x': 'x', 'root.users.user_1.accelerometer.y': 'y', 'root.users.user_1.accelerometer.z': 'z'}, inplace=True)

    gyroscope_data['xBody'] = filterAcceleration(gyroscope_data['x'])
    gyroscope_data['yBody'] = filterAcceleration(gyroscope_data['y'])
    gyroscope_data['zBody'] = filterAcceleration(gyroscope_data['z'])

    accelerometer_data['xBody'] = filterAcceleration(accelerometer_data['x'])
    accelerometer_data['yBody'] = filterAcceleration(accelerometer_data['y'])
    accelerometer_data['zBody'] = filterAcceleration(accelerometer_data['z'])

    accelerometer_data['Time'] = pd.to_datetime(accelerometer_data['Time'], unit='ms')
    gyroscope_data['Time'] = pd.to_datetime(gyroscope_data['Time'], unit='ms')

    merged_df = pd.merge_asof(accelerometer_data, gyroscope_data, on=['Time'], tolerance=pd.Timedelta('200ms'))
    merged_df.dropna(inplace=True)
    merged_df = merged_df.rename(columns={'x_x':'xAcc', 'y_x':'yAcc', 'z_x':'zAcc', 'xBody_x':'xAccBody', 'yBody_x':'yAccBody', 'zBody_x':'zAccBody', 'x_y':'xGyro', 'y_y':'yGyro', 'z_y':'zGyro', 'xBody_y':'xGyroBody', 'yBody_y':'yGyroBody', 'zBody_y':'zGyroBody'})

    return merged_df


def process_data(accelerometer_data: pd.DataFrame, gyroscope_data: pd.DataFrame) -> pd.DataFrame:
    merged_df = get_merged_dataframe(accelerometer_data, gyroscope_data)

    window_length = 128
    overlap_pct = 0.5
    shift = int(window_length * overlap_pct)
    colNames = {
        'body_acc_x': 'xAccBody',
        'body_acc_y': 'yAccBody',
        'body_acc_z':'zAccBody',
        'body_gyro_x': 'xGyroBody',
        'body_gyro_y': 'yGyroBody',
        'body_gyro_z': 'zGyroBody',
        'total_acc_x': 'xAcc',
        'total_acc_y': 'yAcc',
        'total_acc_z': 'zAcc'
    }

    windowNo = 1
    for i in range(0, len(merged_df) - window_length, shift):
        window = merged_df.iloc[i:i+window_length]

        if len(window) < window_length:
            continue

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

    return pd.DataFrame(testDataDict)


def getActivity(testDf, model):
    predicted = model.predict(testDf)
    word_counts = Counter(predicted)

    most_common_word, count = word_counts.most_common(1)[0]
    confidence = round(count / len(predicted), 3) if len(predicted) > 0 else 0.0

    return most_common_word, confidence

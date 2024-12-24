import pymongo
import pandas as pd
import numpy as np
import math
from datetime import datetime, timedelta
from scipy.stats import median_abs_deviation, entropy
from processingFunctions import filterAcceleration, findFFT,findAmplitude, maxInds, findMagnitudeGravity,findMagnitudeBodyJerk, findBodyJerk, findSMAMagnitude,findMad, findMagnitudeBody, filterGravity, findSMA, findEnergy, findQuantile, findEntropy, findArCoeff
from scipy.fft import fft


startTimestamp = "2023-05-12 16:41:24.750000"
endTimestamp = "2023-05-12 17:00:28.000000"
dtMongoStart = datetime.strptime(startTimestamp, '%Y-%m-%d %H:%M:%S.%f') - timedelta(hours=3)
dtMongoEnd = datetime.strptime(endTimestamp, '%Y-%m-%d %H:%M:%S.%f') - timedelta(hours=3)


uriMongodb = 'mongodb+srv://root:caloriepredictor2023@atlascluster.lyrf4oo.mongodb.net/calaid_android'
client = pymongo.MongoClient(uriMongodb)
db = client['calaid_android']
accelerometerDataCollection = db['AccelerometerData']
gyroscopeDataCollection = db['GyroscopeData']

listAccData = list(accelerometerDataCollection.find({ "userId": "645e41cab22e8213021b5467", "timestamp":{"$gte": dtMongoStart, "$lte": dtMongoEnd} }))
listGyroData = list(gyroscopeDataCollection.find({ "userId": "645e41cab22e8213021b5467", "timestamp":{"$gte": dtMongoStart, "$lte": dtMongoEnd} }))#, "timestamp":{"$gte": dtFiveSec, "$lte": dtMongo}
print(len(listAccData))
dfAccData = pd.DataFrame(listAccData)
dfGyroData = pd.DataFrame(listGyroData)
dfGyroData = dfGyroData.sort_values('timestamp')
dfGyroData['xBody'] = filterAcceleration(dfGyroData['x'])
dfGyroData['yBody'] = filterAcceleration(dfGyroData['y'])
dfGyroData['zBody'] = filterAcceleration(dfGyroData['z'])
print(dfGyroData)
print("--------ACCELEROMETER NEXT-------")
dfAccData = dfAccData.sort_values('timestamp')
dfAccData['xBody'] = filterAcceleration(dfAccData['x'])
dfAccData['yBody'] = filterAcceleration(dfAccData['y'])
dfAccData['zBody'] = filterAcceleration(dfAccData['z'])
print(dfAccData)
merged_df = pd.merge_asof(dfAccData, dfGyroData, on=['timestamp'], tolerance=pd.Timedelta('100ms'))
merged_df.dropna(inplace=True)
merged_df = merged_df.drop(['_id_x', '_id_y','userId_x'], axis=1)
merged_df =merged_df.rename(columns={'x_x':'xAcc', 'y_x':'yAcc', 'z_x':'zAcc', 'xBody_x':'xAccBody', 'yBody_x':'yAccBody', 'zBody_x':'zAccBody', 'x_y':'xGyro', 'y_y':'yGyro', 'z_y':'zGyro', 'xBody_y':'xGyroBody', 'yBody_y':'yGyroBody', 'zBody_y':'zGyroBody'})
print("MERGED DF:----------------------------")
print(merged_df)

#sma, mad, ampl
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
    'total_acc_x': 'xAcc',
    'total_acc_y': 'yAcc',
    'total_acc_z': 'zAcc'
}

windowed_data = []
windowNo = 1
#raport activitate pe zi 
for i in range(0, len(merged_df) - window_length, shift):
    window = merged_df.iloc[i:i+window_length]
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

testDataDF = pd.DataFrame(testDataDict)
print(testDataDF)
testDataDF.to_csv('/mnt/c/Users/sltnm/Desktop/FACULTATE/LICENTA/data_processing_calaid/phase2/merged.csv', encoding='utf-8', index=False)

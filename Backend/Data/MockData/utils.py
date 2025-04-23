import pandas as pd
import os
import numpy as np
from datetime import datetime, timedelta
import pymongo
import certifi
from collections import Counter
from Backend.Data.processingFunctions import findEnergy, findQuantile, findEntropy, findMad, findSMA, findAmplitude, findCorrelation, filterAcceleration
ca = certifi.where()

def prepareData(userId, currentTimestamp):
    dtMongoStart = datetime.strptime(currentTimestamp, '%Y-%m-%d %H:%M:%S.%f') - timedelta(hours=3)
    dtMongoEnd = dtMongoStart - timedelta(minutes=2) 
    print(dtMongoStart)
    print(dtMongoEnd)
    uriMongodb = os.getenv('uriMongodb')
    client = pymongo.MongoClient(uriMongodb, tlsCAFile=ca)
    db = client['calaid_android']
    accelerometerDataCollection = db['AccelerometerData']
    gyroscopeDataCollection = db['GyroscopeData']

    listAccData = list(accelerometerDataCollection.find({ "userId": mongoUserId, "timestamp":{"$gte": dtMongoEnd, "$lte": dtMongoStart} }))
    listGyroData = list(gyroscopeDataCollection.find({ "userId": mongoUserId, "timestamp":{"$gte": dtMongoEnd, "$lte": dtMongoStart} }))#, "timestamp":{"$gte": dtFiveSec, "$lte": dtMongo}

    dfAccData = pd.DataFrame(listAccData)
    dfGyroData = pd.DataFrame(listGyroData)
    dfGyroData = dfGyroData.sort_values('timestamp')
    dfGyroData['xBody'] = filterAcceleration(dfGyroData['x'])
    dfGyroData['yBody'] = filterAcceleration(dfGyroData['y'])
    dfGyroData['zBody'] = filterAcceleration(dfGyroData['z'])

    dfAccData = dfAccData.sort_values('timestamp')
    dfAccData['xBody'] = filterAcceleration(dfAccData['x'])
    dfAccData['yBody'] = filterAcceleration(dfAccData['y'])
    dfAccData['zBody'] = filterAcceleration(dfAccData['z'])

    merged_df = pd.merge_asof(dfAccData, dfGyroData, on=['timestamp'], tolerance=pd.Timedelta('10000ms'))
    merged_df.dropna(inplace=True)
    merged_df = merged_df.drop(['_id_x', '_id_y','userId_x'], axis=1)
    merged_df = merged_df.rename(columns={'x_x':'xAcc', 'y_x':'yAcc', 'z_x':'zAcc', 'xBody_x':'xAccBody', 'yBody_x':'yAccBody', 'zBody_x':'zAccBody', 'x_y':'xGyro', 'y_y':'yGyro', 'z_y':'zGyro', 'xBody_y':'xGyroBody', 'yBody_y':'yGyroBody', 'zBody_y':'zGyroBody'})

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

    for i in range(0, len(merged_df) - window_length, shift):
        window = merged_df.iloc[i:i+window_length]
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
    return testDataDF


def getActivity(testDf, model):
    predicted = model.predict(testDf)
    word_counts = Counter(predicted)
    most_common_word, count = word_counts.most_common(1)[0]
    return most_common_word

def calculateCalories(activity, userWeight):
    mets = 0.0
    if(activity == 'WALKING'):
        mets = 3.5
    elif(activity == 'WALKING_UPSTAIRS'):
        mets = 9.0
    elif(activity == 'WALKING_DOWNSTAIRS'):
        mets = 3.0
    elif(activity == 'SITTING'):
        mets = 1
    elif(activity == 'STANDING'):
        mets = 2.0
    elif(activity == 'LAYING'):
        mets = 1.0
    return 1.05 * mets * 0.033 * userWeight

def addToDatabase(userId, endTimestamp, activityType, caloriesBurned):
    uriMongodb = os.getenv('uriMongodb')
    client = pymongo.MongoClient(uriMongodb, tlsCAFile=ca)
    db = client['calaid_android']
    activityDataCollection = db['ActivityData']
    endTimestamp = datetime.strptime(endTimestamp, '%Y-%m-%d %H:%M:%S.%f')
    startTimestamp = endTimestamp - timedelta(milliseconds=300000) 
    activityDataDoc = {
        "startTimestamp":startTimestamp,
        "endTimestamp": endTimestamp,
        "userId": userId,
        "activityType": activityType,
        "caloriesBurned": caloriesBurned
    }
    activityDataCollection.insert_one(activityDataDoc)
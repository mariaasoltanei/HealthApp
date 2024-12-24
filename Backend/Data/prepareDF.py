import pandas as pd
import numpy as np
from Backend.NewTestDataProcessing.DataPreprocessing.processingFunctions import findEnergy, findQuantile, findEntropy, findMad, findSMA, findAmplitude, findCorrelation

def prepareDataFame(dfType):
    path = "uci_har_dataset/"
    filesPaths = [
        path + dfType + "/Inertial Signals/body_acc_x_" + dfType + ".txt",
        path + dfType + "/Inertial Signals/body_acc_y_" + dfType + ".txt",
        path + dfType + "/Inertial Signals/body_acc_z_" + dfType + ".txt",
        
        path + dfType + "/Inertial Signals/body_gyro_x_" + dfType + ".txt",
        path + dfType + "/Inertial Signals/body_gyro_y_" + dfType + ".txt",
        path + dfType + "/Inertial Signals/body_gyro_z_" + dfType + ".txt",

        path + dfType + "/Inertial Signals/total_acc_x_" + dfType + ".txt",
        path + dfType + "/Inertial Signals/total_acc_y_" + dfType + ".txt",
        path + dfType + "/Inertial Signals/total_acc_z_" + dfType + ".txt",
]

    dictionary = {
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
    for trainFile in filesPaths:
        print(trainFile)
        if("body_acc" in trainFile):
            columnName = trainFile.split("/")[3][0:10]
        else:
            columnName = trainFile.split("/")[11][0:11]

        f = open(trainFile)
        lines = f.readlines()
        for line in lines:
            window = line.replace('  ', ' ').strip().split(' ')
            floats = [float(x) for x in window]
            # print(type(floats))
            dictionary[columnName + '_mean'].append(np.mean(floats))
            dictionary[columnName + '_std'].append(np.std(floats))
            dictionary[columnName + '_max'].append(max(floats))
            dictionary[columnName + '_min'].append(min(floats))
            dictionary[columnName + '_energy'].append(findEnergy(floats))
            dictionary[columnName + '_iqr'].append(findQuantile(floats))
            dictionary[columnName + '_sma'].append(findSMA(floats))
            dictionary[columnName + '_mad'].append(findMad(floats))
            dictionary[columnName + '_amplitude'].append(findAmplitude(floats))

    return dictionary


# labelMappingDict = {}
# with open('uci_har_dataset/activity_labels.txt') as f:
#     for line in f.readlines():
#         labelMappingDict[int(line.split()[0])] = line.split()[1]

dfTrain = pd.DataFrame(prepareDataFame("train"))
print(dfTrain)
yTrain = pd.read_csv('uci_har_dataset/train/y_train.txt', header=None)
print(yTrain)

dfTrain['Activity'] = yTrain
dfTrain['ActivityName'] = dfTrain['Activity'].map(labelMappingDict)

dfTrain.to_csv('data_processing_calaid/phase2/train.csv', index=False)

dfTest = pd.DataFrame(prepareDataFame("test"))
print(dfTest)
yTest = pd.read_csv('uci_har_dataset/test/y_test.txt', header=None)
print(yTest)
dfTest['Activity'] = yTest
dfTest['ActivityName'] = dfTest['Activity'].map(labelMappingDict)

dfTest.to_csv('data_processing_calaid/phase2/test.csv', index=False)

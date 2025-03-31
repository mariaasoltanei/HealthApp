import numpy as np
import pandas as pd
from sklearn import svm, utils, metrics
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC, LinearSVC
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from datetime import datetime
from sklearn import linear_model
from sklearn.ensemble import BaggingClassifier, RandomForestClassifier, AdaBoostClassifier
import matplotlib.pyplot as plt

def trainModel(train_x, train_y, model_name='NB', validation=None):
    model = None
    if model_name == 'LSVC':
        model = LinearSVC(C=30, dual=False, penalty ='l2')
    elif model_name == 'MLP':
        model = MLPClassifier(hidden_layer_sizes=(100,100,100), max_iter=800, alpha=0.0001,
                     solver='sgd', verbose=10, tol=0.000000001)
    elif model_name == 'ADA':
        model = AdaBoostClassifier(n_estimators=50)
    elif model_name == 'BAG':
        model = BaggingClassifier(n_jobs=2, n_estimators=50)
    elif model_name == 'RF':
        model = RandomForestClassifier(n_estimators=200, max_depth=10)
    elif model_name == 'KNN':
        model = KNeighborsClassifier(n_neighbors=5, weights='distance', algorithm='auto', leaf_size=30, p=2, metric='minkowski', metric_params=None, n_jobs=None)
    else:
        model = GaussianNB()
    
    model.fit(train_x, train_y)
    
    if validation is not None:
        y_hat = model.predict(validation[0])
        print(y_hat)
        acc = metrics.accuracy_score(validation[1], y_hat)
        print(f"Validation Accuracy in '{model_name}' = {acc}")
        cm = metrics.confusion_matrix(validation[1], y_hat)
        print(cm)
        recall = cm[0][0] / (cm[0][0] + cm[0][1])
        precision = cm[0][0] / (cm[0][0] + cm[1][0])
        f1 = 2*(precision*recall)/(precision+recall)
        print(f"Recall in '{model_name}' = {recall}")
        print(f"Precision in '{model_name}' = {precision}")
        print(f"F1 Score in '{model_name}' = {f1}")
               
    return model

def perform_model(model, X_train, y_train, X_test, y_test, class_labels, cm_normalize=True, \
                 print_cm=True, cm_cmap=plt.cm.Greens):

    results = dict()
    model.fit(X_train, y_train)

    print('Predicting test data')
    y_pred = model.predict(X_test)
    results['predicted'] = y_pred
    print("Y PREDICTED", y_pred)
    accuracy = metrics.accuracy_score(y_true=y_test, y_pred=y_pred)
    results['accuracy'] = accuracy
    print('|Accuracy|')
    print('{}\n\n'.format(accuracy))
    
    
    # confusion matrix
    cm = metrics.confusion_matrix(y_test, y_pred)
    results['confusion_matrix'] = cm
    if print_cm: 
        print('|Confusion Matrix|')
        print('\n {}'.format(cm))
        
    print('|Classifiction Report|')
    classification_report = metrics.classification_report(y_test, y_pred)
    results['classification_report'] = classification_report
    print(classification_report)
    
    # add the trained  model to the results
    results['model'] = model
    
    return results

def print_grid_search_attributes(model):

    print('|Best Estimator|')
    print('\n\t{}\n'.format(model.best_estimator_))

    print('\tParameters of best estimator : \n\n\t{}\n'.format(model.best_params_))

    print('|No of CrossValidation sets|')
    print('\n\tTotal no of cross validation sets: {}\n'.format(model.n_splits_))
    print('|Best Score|')
    print('\n\tAverage Cross Validate scores of best estimator : \n\n\t{}\n'.format(model.best_score_))

dfTrain = pd.read_csv('/mnt/c/Users/sltnm/Desktop/FACULTATE/LICENTA/data_processing_calaid/phase2/train.csv')
dfTest = pd.read_csv('/mnt/c/Users/sltnm/Desktop/FACULTATE/LICENTA/data_processing_calaid/phase2/merged.csv')
print(dfTrain.sample())
print(dfTest.sample())
X_train = dfTrain.drop(['Activity', 'ActivityName'], axis=1)
y_train = dfTrain.ActivityName
X_test = dfTest#.drop(['Activity', 'ActivityName'], axis=1)
# y_test = dfTest.ActivityName
print('X_train and y_train : ({},{})'.format(X_train.shape, y_train.shape))
print('X_test  and y_test  :', X_test.shape)



labels=['LAYING', 'SITTING','STANDING','WALKING','WALKING_DOWNSTAIRS','WALKING_UPSTAIRS']
# parameters = {'C':[0.01, 0.1, 30], 'penalty':['l2','l1'], 'dual' :[True, False], 'tol':[0.00000001,0.000000001], 'multi_class':['crammer_singer', 'ovr']}
# #BEST ESTIMATOR: SVC(C=30, kernel='linear')
# # log_reg = LinearSVC() #LinearRegression
# # log_reg_grid = GridSearchCV(log_reg, param_grid=parameters, cv=3, verbose=1, n_jobs=-1)
# # log_reg_grid_results =  perform_model(log_reg_grid, X_train, y_train, X_test, y_test, class_labels=labels)
# # print_grid_search_attributes(log_reg_grid_results['model'])

# parameters = {'C':[0.01, 0.1, 1, 10, 20, 30], 'penalty':['l2','l1']}
# log_reg = linear_model.LogisticRegression()
# log_reg_grid = GridSearchCV(log_reg, param_grid=parameters, cv=3, verbose=1, n_jobs=-1)
# log_reg_grid_results =  perform_model(log_reg_grid, X_train, y_train, X_test, y_test, class_labels=labels)
# print_grid_search_attributes(log_reg_grid_results['model'])

# model1 = trainModel(X_train, y_train, model_name='ADA', validation=(X_test, y_test))

# model2 = trainModel(X_train, y_train, model_name='BAG', validation=(X_test, y_test))

model3 = trainModel(X_train, y_train, model_name='LSVC', validation=(X_test, None))

# model4 = trainModel(X_train, y_train, model_name='MLP', validation=(X_test, y_test))

# model5 = trainModel(X_train, y_train, model_name='KNN', validation=(X_test, y_test))

import os
import random

import numpy as np
import pandas as pd
import sklearn.metrics
from sklearn import svm
from joblib import dump

# origin_path = '/Users/sanjanacheerla/IOT/hw4/door_data'
origin_path = '/home/dhnguye4/IOT/hw4/door_data'
paths = ['/close/22p5degrees/', '/close/45degrees/', '/close/67p5degrees/', '/close/90degrees/', '/open/22p5degrees/', '/open/45degrees/', '/open/67p5degrees/', '/open/90degrees/']
files = []

# get all the files in the data folder
for path in paths:
    for filename in os.listdir(origin_path + path):
        f = os.path.join((origin_path + path), filename)
        # checking if it is a file
        if os.path.isfile(f):
            files.append(f)

# get the data shaped into an averagedd nd numpy array
# and a numerical array for the open and close labels
# 0 is close, 1 is open
data_combined = []
values = []
for file in files:
    data = pd.read_csv(file)
    tmp_val = 0
    if "close" in file:
        tmp_val = 0
    if "open" in file:
        tmp_val = 1

    data.columns=['ax', 'ay', 'az', 'gx', 'gy', 'gz']
    data = data.to_numpy()
    v = np.mean(data, axis=0)
    v = np.append(v, [tmp_val])
    data_combined.append(v)

# shuffle data for classifier
random.shuffle(data_combined)

# split data and labels
modified_data = []
for i in data_combined:
    values.append(i[6])
    modified_data.append(np.delete(i, -1))

# split into test and training data
split_val = 40
x_train = modified_data[:split_val]
y_train = values[:split_val]

x_test = modified_data[split_val:]
y_test = values[split_val:]

# Create a SVM classifier
clf = svm.LinearSVC(dual=False)
clf.fit(x_train, y_train)

# Export the trained model
dump(clf, 'door_model.joblib')
# Test the model using some sample data from the test files
# print(str(clf.predict([[-3.5267175572519083,0.2748091603053435,-0.3053435114503817,1.01611328125,-0.055419921875,0.114013671875]])))



def analyze_resuts(x_train, y_train, x_test, y_test): 
    acc1 = clf.score(x_train, y_train)
    acc2 = clf.score(x_test, y_test)

    print("Baseline accuracy: " + str(acc1))
    print("Tested accuracy: " + str(acc2))

    # predict and print out the predicted values
    y_pred = clf.predict(x_test)
    # for i in range(len(y_pred)):
    #         print(y_pred[i])

    labels = [0,1]

    report = sklearn.metrics.classification_report(
        y_test, y_pred, digits=5, labels=labels
    )

    print("Classification report:")
    print(report)

    cm = sklearn.metrics.confusion_matrix(y_test, y_pred, labels=labels)

    print("Confusion matrix:")
    print(cm)
    print()

analyze_resuts(x_train, y_train, x_test, y_test)

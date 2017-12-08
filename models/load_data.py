import pandas as pd
import numpy as np
import math

trainPct = .9
testPct = .1


def load_data() -> dict:
    """
    Load the data.csv file into a dictionary of train and test data.

    :return: a dictinary containing train and test data sets
    :rtype: dictionary
    """
    filename = '../database-generator/data.csv'
    print("Loading data from ", filename, "...")

    dataFrame = pd.read_csv(filename, dtype=np.float)
    data = dataFrame.values

    numExamples = data.shape[0]
    numFeatures = data.shape[1] - 1
    print("\tFeatures=", numFeatures, "Examples=", numExamples)

    assert numExamples > 50
    assert numFeatures > 0

    numTrain = math.floor(numExamples * trainPct)
    numTest = math.floor(numExamples * testPct)
    print("\tnumTrain=", numTrain, "numTest=", numTest)

    # print("Converting and slicing", numExamples, "examples for numpy ...")
    # data = np.array(data, dtype=float)
    test_data = data[:numTest, :-1]
    test_label = data[:numTest, -1]
    train_data = data[numTest:numTest + numTrain, :-1]
    train_label = data[numTest:numTest + numTrain, -1]

    modelParams = dict()
    modelParams['train_data'] = train_data
    modelParams['train_label'] = train_label
    modelParams['test_data'] = test_data
    modelParams['test_label'] = test_label
    return modelParams


if __name__ == '__main__':
    from datetime import datetime
    start = datetime.now()
    load_data()
    dur = datetime.now() - start
    print("Load Data complete in", dur, "time")

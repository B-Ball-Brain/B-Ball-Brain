import fileUtilities
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn import svm
from sklearn import ensemble
from sklearn.metrics import mean_squared_error
from time import time
import random
import numpy as np

random.seed(100)
np.random.seed(100)

TEST_PERCENT = .10


def getNewModel():
    yield linear_model.LinearRegression()
    yield linear_model.BayesianRidge()
    yield linear_model.RidgeCV(alphas=[0.1, 1.0, 10.0])
    yield linear_model.ElasticNetCV(alphas=[0.1, 1.0, 10.0])
    yield linear_model.LassoCV(alphas=[0.1, 1.0, 10.0])
    yield ensemble.GradientBoostingRegressor(n_estimators=1)
    yield ensemble.GradientBoostingRegressor(n_estimators=2)
    yield ensemble.GradientBoostingRegressor(n_estimators=4)
    yield ensemble.GradientBoostingRegressor(n_estimators=8)
    yield ensemble.AdaBoostRegressor(n_estimators=1)
    yield ensemble.AdaBoostRegressor(n_estimators=2)
    yield ensemble.AdaBoostRegressor(n_estimators=4)
    yield ensemble.AdaBoostRegressor(n_estimators=8)
    yield ensemble.ExtraTreesRegressor(n_estimators=2)
    yield ensemble.RandomForestRegressor(n_estimators=2)
    ''' can take 5+ mins ...'''
    # yield svm.SVR()


def main():
    data = fileUtilities.getDataFromCSV()
    x = data[:, :-1]
    y = data[:, -1]
    x = preprocessing.scale(x)
    trainX, testX, trainY, testY = train_test_split(x, y, test_size=TEST_PERCENT)
    numFeatures = trainX.shape[1]
    trainSize = trainX.shape[0]
    testSize = testX.shape[0]
    assert trainSize > 50
    assert testSize > 0
    assert numFeatures > 0
    print("\t Features:{} \t TrainSize={} \t TestSize={}".format(numFeatures, trainSize, testSize))

    for model in getNewModel():
        model.name = str(model).split('(')[0]
        trainModel(model, trainX, trainY)
        testModel(model, testX, testY)
        printModelResults(model)


def trainModel(model, trainData, trainLabels):
    print("Training with", model.name, "...")
    start = time()
    model.fit(trainData, trainLabels)
    model.trainDuration = time() - start
    trainPredictions = model.predict(trainData)
    model.trainMSE = mean_squared_error(trainLabels, trainPredictions)


def testModel(model, testData, testLabels):
    print("Testing with", model.name, "...")
    testPredictions = model.predict(testData)
    model.testMSE = mean_squared_error(testLabels, testPredictions)


def printModelResults(model):
    name = model.name
    estimators = model.get_params().get('n_estimators', 0)
    if estimators > 0:
        name += ", est=" + str(estimators)
    dur = "{0:.3f}".format(model.trainDuration)
    trainMSE = "{0:.3f}".format(model.trainMSE)
    testMSE = "{0:.3f}".format(model.testMSE)
    outputs = name, dur, trainMSE, testMSE
    print("\t{} took {} secs with MSEs of {} and {}".format(*outputs))


if __name__ == '__main__':
    main()

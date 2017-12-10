import fileUtilities
from sklearn import preprocessing
#from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn import ensemble
from sklearn import svm
from sklearn import dummy
from sklearn.metrics import mean_squared_error, r2_score
from time import time
import random
import numpy as np

random.seed(100)
np.random.seed(100)

#TEST_PERCENT = .20


def getNewModel():
    alphas = [2**x for x in range(-7, 4)]
    #estimators = [1, 2, 4, 10, 20, 50, 100]
    yield dummy.DummyRegressor()
    yield linear_model.LinearRegression()
    yield linear_model.BayesianRidge()
    yield linear_model.RidgeCV(alphas=alphas)
    yield linear_model.ElasticNetCV(alphas=alphas)
    yield linear_model.LassoCV(alphas=alphas)
    yield ensemble.GradientBoostingRegressor(n_estimators=10)
    yield ensemble.AdaBoostRegressor(n_estimators=10)
    #yield ensemble.ExtraTreesRegressor(n_estimators=10)
    yield ensemble.RandomForestRegressor(n_estimators=10)
    #yield svm.LinearSVR()
    ''' can take 5+ mins below ...'''
    #yield svm.SVR(kernel='rbf')


def main():
    train_data, test_data, synthetic_data = fileUtilities.getDataFromCSV()
    trainX = train_data[:, :-1]
    trainY = train_data[:, -1]
    scaler = preprocessing.StandardScaler().fit(trainX)
    trainX = scaler.transform(trainX)

    testX = test_data[:, :-1]
    testY = test_data[:, -1]
    testX = scaler.transform(testX)
    #trainX, testX, trainY, testY = train_test_split(x, y, test_size=TEST_PERCENT)
    numFeatures = trainX.shape[1]
    trainSize = trainX.shape[0]
    testSize = testX.shape[0]
    assert trainSize > 50
    assert testSize > 0
    assert numFeatures > 0
    print("\t Features:{} \t TrainSize={} \t TestSize={}".format(numFeatures, trainSize, testSize))

    model_list = []

    with open("ModelResults.csv", 'w') as outFile:
        headers = "Full Name,Alpha,Estimators,Duration,TrainSize,TrainMSE,TrainRMSE,TestSize,TestMSE,TestRMSE,R^2 Score\n"
        outFile.write(headers)

        for model in getNewModel():
            model.name = str(model).split('(')[0]
            trainModel(model, trainX, trainY)
            model_list.append(model)
        print("\n")
        for model in model_list:
            testModel(model, testX, testY)
            printModelResults(model)
            outFile.write(getOutputModelString(model) + '\n')
        print("\n")
        for model in model_list:
        	makeIndividualPredictions(model, synthetic_data, scaler)


def trainModel(model, trainData, trainLabels):
    print("Training with", model.name, "...")
    model.trainSize = trainData.shape[0]
    start = time()
    model.fit(trainData, trainLabels)
    model.trainDuration = time() - start
    trainPredictions = model.predict(trainData)
    model.trainMSE = mean_squared_error(trainLabels, trainPredictions)
    model.trainRMSE = np.sqrt(model.trainMSE)


def testModel(model, testData, testLabels):
    print("Testing with", model.name, "...")
    model.testSize = testData.shape[0]
    testPredictions = model.predict(testData)
    model.testMSE = mean_squared_error(testLabels, testPredictions)
    model.score = r2_score(testLabels, testPredictions)
    model.testRMSE = np.sqrt(model.testMSE)


def printModelResults(model):
    name = model.name
    estimators = model.get_params().get('n_estimators', 0)
    if estimators > 0:
        name += ", est=" + str(estimators)
    dur = "{0:.3f}".format(model.trainDuration)
    trainMSE = "{0:.3f}".format(model.trainMSE)
    testMSE = "{0:.3f}".format(model.testMSE)
    score = "{0:.3f}".format(model.score)
    outputs = name, dur, trainMSE, testMSE, score
    print("\t{} took {} secs with MSEs of {} and {} and R^2 of {}".format(*outputs))


def getOutputModelString(m):
    # headers = "Name,Alpha,Estimators,Duration,TrainSize,TrainMSE,TestSize,TestMSE,r^2"
    # alphas = m.get_params().get('alphas', [])
    alpha = getattr(m, 'alpha_', '')
    estimator = m.get_params().get('n_estimators', '')
    #fullName = m.name + str(estimator)
    fullName = m.name
    output = [fullName]
    output.append(alpha)
    output.append(estimator)
    output.append(m.trainDuration)
    output.append(m.trainSize)
    output.append(m.trainMSE)
    output.append(m.trainRMSE)
    output.append(m.testSize)
    output.append(m.testMSE)
    output.append(m.testRMSE)
    output.append(m.score)
    return ','.join([str(val) for val in output])


def makeIndividualPredictions(model, s_data, scaler):
	testPredictions = model.predict(scaler.transform(s_data))
	formattedPred = ["{:0.3f}".format(member) for member in testPredictions]
	print("Testing synthetic data with", model.name, "gives the predictions", formattedPred)


if __name__ == '__main__':
    main()

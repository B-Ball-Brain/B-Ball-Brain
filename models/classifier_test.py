import fileUtilities
from sklearn import preprocessing
from time import time
import pandas
import numpy as np
from pandas.tools.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

# TEST_PERCENT = 0.2

def getNewModel():
    # yield LogisticRegression(C = 0.01, tol=1.0e-4)
    # yield LinearDiscriminantAnalysis()
    # yield KNeighborsClassifier(n_neighbors = 10, weights='distance')
    # yield MLPClassifier(hidden_layer_sizes=(64, 12, 12, 8), solver = 'adam', activation='logistic', alpha=0.01, max_iter=400)
    # yield GaussianNB()
    yield SVC(kernel='linear', C = 1)
    # yield SVC(kernel='rbf')
    # yield GradientBoostingClassifier()
    # yield RandomForestClassifier()
    
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

    trainY[trainY >= 0] =  1
    trainY[trainY < 0]  = -1
    testY[testY >= 0]   =  1
    testY[testY < 0]    = -1
    
    print(trainY)
    
    numFeatures = trainX.shape[1]
    trainSize   = trainX.shape[0]
    testSize    = testX.shape[0]

    assert trainSize > 50
    assert testSize > 0
    assert numFeatures > 0
    print("\t Features:{} \t TrainSize={} \t TestSize={}".format(numFeatures, trainSize, testSize))

    model_list = []

    with open("ModelResults.csv", 'w') as outFile:
        headers = "Full Name,Duration,TrainSize,TrainAccuracy,TestSize,TestAccuracy\n"
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
        # for model in model_list:
        #     makeIndividualPredictions(model, synthetic_data)


def trainModel(model, trainData, trainLabels):
    print("Training with", model.name, "...")
    model.trainSize = trainData.shape[0]
    start = time()
    model.fit(trainData, trainLabels)
    model.trainDuration = time() - start
    trainPredictions    = model.predict(trainData)
    model.trainAccuracy = accuracy_score(trainLabels, trainPredictions)
    model.classReport   = classification_report(trainLabels, trainPredictions)


def testModel(model, testData, testLabels):
    print("Testing with", model.name, "...")
    model.testSize  = testData.shape[0]
    testPredictions = model.predict(testData)
    print(testPredictions)
    model.testAccuracy = accuracy_score(testLabels, testPredictions)
    model.confMatrix   = confusion_matrix(testLabels, testPredictions)
    print(classification_report(testLabels, testPredictions))


def printModelResults(model):
    name = model.name
    estimators = model.get_params().get('n_estimators', 0)
    if estimators > 0:
        name += ", est=" + str(estimators)
        dur   = "{0:.3f}".format(model.trainDuration)
        trainAccuracy = "{0:.3f}".format(model.trainAccuracy)
        testAccuracy  = "{0:.3f}".format(model.testAccuracy)
        outputs = name, dur, trainAccuracy, testAccuracy
        print("\t{} took {} secs with train accuracy of {} and test accuracy of {}".format(*outputs))


def getOutputModelString(m):
    alpha = getattr(m, 'alpha_', '')
    estimator = m.get_params().get('n_estimators', '')
    fullName  = m.name
    output    = [fullName]
    output.append(m.trainDuration)
    output.append(m.trainSize)
    output.append(m.trainAccuracy)
    output.append(m.testSize)
    output.append(m.testAccuracy)
    return ','.join([str(val) for val in output])


def makeIndividualPredictions(model, s_data):
    #testPredictions = model.predict(scaler.transform(s_data))
    testPredictions = model.predict(s_data)
    formattedPred = ["{:0.3f}".format(member) for member in testPredictions]
    print("Testing synthetic data with", model.name, "gives the predictions", formattedPred)


if __name__ == '__main__':
    main()

import pandas as pd
import numpy as np
from time import time


def getDataFromCSV():
    """
    Load the data.csv file into train and test data
    """
    start = time()
    trainfile = '../database-generator/data.csv'
    testfile = '../database-generator/testdata.csv'
    syntheticfile = '../database-generator/synthetic.csv'
    print("Loading training and test data from %s and %s ..." % (trainfile, testfile))

    dataFrame = pd.read_csv(trainfile, dtype=np.float, header=None)
    train_data = dataFrame.values

    dataFrame = pd.read_csv(testfile, dtype=np.float, header=None)
    test_data = dataFrame.values

    dataFrame = pd.read_csv(syntheticfile, dtype=np.float, header=None)
    synthetic_data = dataFrame.values

    dur = time() - start
    print("Train and test data loaded in {0:.3f} seconds".format(dur))
    return train_data, test_data, synthetic_data


if __name__ == '__main__':
    getDataFromCSV()


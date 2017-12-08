import pandas as pd
import numpy as np
from time import time


def getDataFromCSV():
    """
    Load the data.csv file into train and test data
    """

    start = time()
    filename = '../database-generator/data.csv'
    print("Loading data from ", filename, "...")

    dataFrame = pd.read_csv(filename, dtype=np.float)
    data = dataFrame.values

    dur = time() - start
    print("Load from CSV complete in {0:.3f} seconds".format(dur))
    return data


if __name__ == '__main__':
    getDataFromCSV()

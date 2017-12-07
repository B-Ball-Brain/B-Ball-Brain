"""Function for loading csv file"""
import numpy as np
import csv


def load_data():
    """
    Load the data.csv file into a dictionary of train and test data.

    :return: a dictinary containing train and test data sets
    :rtype: dictionary
    """
    data = dict()
    filename = '../database-generator/data.csv'
    data_rows = []

    with open(filename) as csv_data:
        csv_file = csv.reader(csv_data)
        for row in csv_file:
            data_rows.append(row)

    #To speed up training/test, uncomment/comment to use less training and test samples
    row_data = np.array(data_rows, dtype=float)
    train_data = row_data[:23272,:-1]
    #train_data = row_data[:10000,:-1]
    train_label = row_data[:23272,-1]
    #train_label = row_data[:10000,-1]
    test_data = row_data[23272:,:-1]
    #test_data = row_data[26590:,:-1]
    test_label = row_data[23272:,-1]
    #test_label = row_data[26590:,-1]   
    data['train_data'] = train_data
    data['train_label'] = train_label
    data['test_data'] = test_data
    data['test_label'] = test_label   
    return data

'''
CS 6140 Machine Learning - Assignment 04

Problem 1.3.1 - Linear Kernel Dual Perceptron Classification - Two Spiral Dataset

@author: Rajesh Sakhamuru
@version: 7/20/2020
'''

import pandas as pd
import statistics as st

import perceptronFunctions as pf


def tenFoldCrossValidation(originalData, target, verbose=True):
    '''
    This function generates weights using the perceptron algorithm
    and tests the accuracy of those weights based on 10 unique folds of the 
    dataset provided. Then the accuracy, precision and recall values over the 
    folds and the confusion matrix are returned.
    
    :param originalData: dataframe with all training and testing data 
    :param target: target column name
    :param verbose: if True, will print testing results per fold
    '''
    # prevent changes to original data
    data = originalData.copy()

    # shuffle data
    dataShuffled = data.sample(frac=1).reset_index(drop=True)
    numRows = len(dataShuffled)

    oneTenthRows = round(numRows / 10)

    # list of loss values and accuracy, precison and recall data over the folds
    trainAccuracyList = []
    testAccuracyList = []
    trainPrecisionList = []
    testPrecisionList = []
    trainRecallList = []
    testRecallList = []

    # empty confusion matrix
    targetCats = data[target].unique()
    confusionDict = {}
    for cat in targetCats:
        confusionDict[cat] = [0] * len(targetCats)
    testConfusionMatrix = pd.DataFrame(data=confusionDict, index=targetCats)
    trainConfusionMatrix = pd.DataFrame(data=confusionDict, index=targetCats)

    # 10-fold cross validation of growTree model
    for n in range(10):

        # split into training and testing data
        testData = dataShuffled[(n * oneTenthRows):oneTenthRows * (n + 1)]
        trainData = dataShuffled.drop(dataShuffled.index[(n * oneTenthRows):oneTenthRows * (n + 1)])

        # normalize training and test data with zscore normalization
        normTrainData, normParams, _ = pf.zScoreNormalization(trainData, target)
        normTestData, _, _ = pf.zScoreNormalization(testData, target, normParams=normParams)

        # calculate weights  and alphas using gradient descent
        alphas = pf.dualPerceptronKernel(normTrainData, target, pf.linearKernel)

        # calculate training and testing accuracy and confusion matrices
        trainAccuracy, trainConfMatrix = pf.calcAccuracyUsingAlphas(normTrainData, normTrainData, target, alphas, pf.linearKernel)
        testAccuracy, testConfMatrix = pf.calcAccuracyUsingAlphas(normTestData, normTrainData, target, alphas, pf.linearKernel)

        # accuracy and recall calculations
        truePos = trainConfMatrix.at[1, 1]
        falseNeg = trainConfMatrix.at[-1, 1]
        falsePos = trainConfMatrix.at[1, -1]
        trainPrecisionList.append(truePos / (truePos + falsePos))
        trainRecallList.append(truePos / (truePos + falseNeg))

        truePos = testConfMatrix.at[1, 1]
        falseNeg = testConfMatrix.at[-1, 1]
        falsePos = testConfMatrix.at[1, -1]
        testPrecisionList.append(truePos / (truePos + falsePos))
        testRecallList.append(truePos / (truePos + falseNeg))

        trainAccuracyList.append(trainAccuracy)
        testAccuracyList.append(testAccuracy)

        # confusion matrix addition
        trainConfusionMatrix = pd.concat([trainConfusionMatrix, trainConfMatrix], sort=True).groupby(level=0).sum()
        testConfusionMatrix = pd.concat([testConfusionMatrix, testConfMatrix], sort=True).groupby(level=0).sum()

        if verbose:
            print("\nFold #", n + 1)
            print("Accuracy for normalized data using Dual Perceptron Algorithm w/ linear kernel:")
            print('Train Accuracy:', trainAccuracy)
            print('Test Accuracy:', testAccuracy)
            print("---------------------------------------------------")

    # reslults coallated into a dataframe and returned
    mean = st.mean(trainAccuracyList)
    stdDev = st.stdev(trainAccuracyList)
    trainAccuracyList.append(mean)
    trainAccuracyList.append(stdDev)

    mean = st.mean(testAccuracyList)
    stdDev = st.stdev(testAccuracyList)
    testAccuracyList.append(mean)
    testAccuracyList.append(stdDev)

    mean = st.mean(trainPrecisionList)
    stdDev = st.stdev(trainPrecisionList)
    trainPrecisionList.append(mean)
    trainPrecisionList.append(stdDev)

    mean = st.mean(trainRecallList)
    stdDev = st.stdev(trainRecallList)
    trainRecallList.append(mean)
    trainRecallList.append(stdDev)

    mean = st.mean(testPrecisionList)
    stdDev = st.stdev(testPrecisionList)
    testPrecisionList.append(mean)
    testPrecisionList.append(stdDev)

    mean = st.mean(testRecallList)
    stdDev = st.stdev(testRecallList)
    testRecallList.append(mean)
    testRecallList.append(stdDev)

    resultsTable = pd.DataFrame()
    resultsTable["Fold #"] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'Mean', 'Std Deviation']
    resultsTable["Train Accuracy"] = trainAccuracyList
    resultsTable["Train Precision"] = trainPrecisionList
    resultsTable["Train Recall"] = trainRecallList
    resultsTable["Test Accuracy"] = testAccuracyList
    resultsTable["Test Precision"] = testPrecisionList
    resultsTable["Test Recall"] = testRecallList

    return resultsTable, trainConfusionMatrix, testConfusionMatrix


def main():
    # data visualization options for console output
    pd.set_option('display.max_columns', None)
#     pd.set_option('display.max_rows', None)
    pd.set_option('display.expand_frame_repr', False)
    # import data file

    colNames = range(3)
    try:
        spirData = pd.read_csv("datasets/twoSpirals.csv", names=colNames)
    except:
        print("File not found")

    # add constant feature for w0
    spirData.insert(0, 'constant', 1)
    spirData.columns = range(4)

    target = spirData.columns[-1]

    print(spirData)

    resultsTable, trainConfusionMatrix, testConfusionMatrix = \
    tenFoldCrossValidation(spirData, target, verbose=True)

    print("Results Table:")
    print(resultsTable)

    print("\nColumns are actual value, Rows are predicted value")
    print("Training Confusion Matrix:")
    print(trainConfusionMatrix)

    print("\nTesting Confusion Matrix:")
    print(testConfusionMatrix)

'''



































'''

main()
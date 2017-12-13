import fileUtilities
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model

def plotAnalysis():
    train_data, test_data, synthetic_data = fileUtilities.getDataFromCSV()
    col_headers = 'age, gp, w, l, win %, min, fgm, fga, fgPct, fG3M, fG3A, fg3Pct, ftm, fta, ftPct, oreb, dreb, reb, ast, tov, stl, blk, blka, pf, pfd, pts, +/-, nbaFantasyPts, dD2, tD3, gpRank, wRank, lRank, wPctRank, minRank, fgmRank, fgaRank, fgPctRank, fg3mRank, fg3aRank, fg3PctRank, ftmRank, ftaRank, ftPctRank, orebRank, drebRank, rebRank, astRank, tovRank, stlRank, blkRank, blkaRank, pfRank, pfdRank, ptsRank, plusMinusRank, nbaFantasyPtsRank, dd2Rank, td3Rank, cfid'.split(', ')
    trainX = train_data[:, :-1]
    trainY = train_data[:, -1]

    avgMatrix = np.kron(np.identity(2), np.kron(np.ones((5, 1)), np.identity(60))) / 5
    averagedTrain = trainX.dot(avgMatrix)

    diffAveragedTrain = averagedTrain.dot(np.block([[np.identity(60)], [-np.identity(60)]]))

    index = 4;

    scatterX = trainY
    scatterY = diffAveragedTrain[:, index]

    plotX = np.linspace(np.min(scatterX), np.max(scatterX)).reshape(-1,1)
    plotY = linear_model.LinearRegression().fit(scatterX.reshape(-1, 1), scatterY).predict(plotX)

    plt.scatter(trainY, scatterY, label = "Time capsules")
    plt.xlabel('+/- per minute')
    plt.ylabel("Average " + col_headers[index] + " differential (home - away)")
    plt.plot(plotX, plotY, 'r', linewidth = 2.0, label = "Best-fit line")
    plt.legend()
    plt.show()

if __name__ == '__main__':
    plotAnalysis()

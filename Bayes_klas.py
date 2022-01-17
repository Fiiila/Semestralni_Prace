import math

import numpy as np
import matplotlib.pyplot as plt

from Agl_m_v01 import nactiDataDoPole, vykresliDataPodleLabelu


def trainBayes(data, labels):

    tridy = np.unique(labels)
    pocetTrid = len(tridy)
    mnoziny = [data[labels==i]for i in range(pocetTrid)]

    #vypocet parametru normalniho rozlozeni
    stredniHodnoty = [np.mean(mnozina,axis=0)for mnozina in mnoziny]
    covMat = [np.cov(mnozina.T)for mnozina in mnoziny]

    #apriorni ppsti jednotlivych mnozin
    aprPpsti = [len(mnozina)/len(data) for mnozina in mnoziny]

    return stredniHodnoty, covMat, aprPpsti

def clasifBayes(body, strHod, covMat, aprPpsti):
    pocetBodu = len(body)
    pocetTrid = len(strHod)
    labels = np.zeros(pocetBodu,dtype=int)
    for i in range(pocetBodu):
        tempLabel = np.zeros(pocetTrid)
        for trida in range(pocetTrid):
            tempLabel[trida] = spoctiPpst(body[i],strHod[trida],covMat[trida])*aprPpsti[trida]
        labels[i] = np.argmax(tempLabel)

    return labels

def spoctiPpst(bod, strHod, covMat):
    n = len(bod)
    diff = bod-strHod
    invCovMat = np.linalg.inv(covMat)
    detCovMat = np.linalg.det(covMat)
    expPart = math.exp(-1/2*diff.T.dot(invCovMat).dot(diff))
    ppst = 1/(math.sqrt((2*math.pi)**n * (detCovMat)))*expPart
    return ppst
def clasifGrid(body, strHod, covMat, aprPpsti):
    noStep = 50
    xmin, xmax = np.min(body[:,0]), np.max(body[:,0])
    xStep = np.abs(xmax-xmin)/noStep
    ymin, ymax = np.min(body[:, 1]), np.max(body[:, 1])
    yStep = np.abs(ymax - ymin) / noStep
    X, Y = np.mgrid[xmin:xmax:xStep, ymin:ymax:yStep]
    grid = np.stack((X.flatten(), Y.flatten()), -1)

    gridLabel = clasifBayes(grid,strHod,covMat,aprPpsti)
    return grid,gridLabel


def loadLabels(filename):
    f = open(filename)
    labels = []
    for line in f:
        labels.append(int(line.strip()))
    f.close()
    return labels

if __name__ == "__main__":
    nazev = 'data'  # "dataTest2"
    X, Y = nactiDataDoPole(nazev)
    labels = np.array(loadLabels('Data/labels.txt'))
    #plt.figure()
    #plt.scatter(X, Y)
    #plt.show()
    data = np.stack((X, Y), axis=-1)
    stredniHodnoty, covMat, aprPpsti = trainBayes(data, labels)
    gridPoints,gridLabel = clasifGrid(data,stredniHodnoty,covMat,aprPpsti)
    #dataLabels = clasifBayes(data,stredniHodnoty,covMat,aprPpsti)
    plt.figure()
    vykresliDataPodleLabelu(gridPoints[:,0],gridPoints[:,1],gridLabel, opacity=0.3)
    #vykresliDataPodleLabelu(data[:, 0], data[:, 1], dataLabels, opacity=1)

    plt.show()

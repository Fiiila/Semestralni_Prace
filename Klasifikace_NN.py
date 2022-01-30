import numpy as np
from matplotlib import pyplot as plt

from Agl_m_v01 import nactiDataDoPole, vykresliDataPodleLabelu, spoctiVzdalenost
from Bayes_klas import loadLabels


def pouzijKNN(trainData, trainLabels, data, K=1):
    '''
    metoda pro klasifikaci podle K nejblizsich sousedu...defaultne nastaveno na 1
    :param trainData: trenovaci data
    :param trainLabels: labely odpovidajici trenovacim datum
    :param data: vstupni data, ktera chceme klasifikovat
    :param K: pocet podle kolika nejblizsich sousedu se ma klasifikator rozhodovat
    :return: vraci labely danych vstupnich dat
    '''
    dataLabels = np.zeros(len(data), dtype=int)
    mnoziny = [trainData[trainLabels == i] for i in range(len(np.unique(trainLabels)))]
    for i in range(len(data)):
        minVzdalenostOdKNN = []
        for mnozina in mnoziny:
            distances = np.zeros(len(mnozina))
            for j in range(len(mnozina)):
                distances[j] = spoctiVzdalenost(data[i], mnozina[j])
            distances = np.sort(distances)
            minVzdalenostOdKNN.append(np.average(distances[0:K]))
        dataLabels[i] = np.argmin(minVzdalenostOdKNN)
    return dataLabels

def makeGrid(xmin,xmax,ymin,ymax,noStep=50):
    '''
    vytvoreni bodu v uskupeni gridu pro vizualizaci klasifikace
    :param xmin: hodnota bodu nejvice vlevo
    :param xmax: hodnota bodu nejvice vpravo
    :param ymin: hodnota bodu nejvice dole
    :param ymax: hodnota bodu nejvice nahore
    :param noStep: pocet kroku mezi hranicnimi body
    :return: flattened array ziskaneho gridu
    '''
    xStep = np.abs(xmax - xmin) / noStep
    yStep = np.abs(ymax - ymin) / noStep
    X, Y = np.mgrid[xmin - xStep:xmax + xStep:xStep, ymin - yStep:ymax + yStep:yStep]
    grid = np.stack((X.flatten(), Y.flatten()), -1)
    return grid

if __name__ == "__main__":
    nazev = "Data/data600"
    X, Y = nactiDataDoPole(nazev)
    labels = np.array(loadLabels('Data/labels600.txt'))
    plt.figure()
    plt.scatter(X, Y)
    plt.show()
    data = np.stack((X, Y), axis=-1)
    xmin, xmax = np.min(data[:, 0]), np.max(data[:, 0])
    ymin, ymax = np.min(data[:, 1]), np.max(data[:, 1])
    grid = makeGrid(xmin,xmax,ymin,ymax,noStep=50)
    gridlabels = pouzijKNN(data,labels,grid,K=1)
    plt.figure()
    vykresliDataPodleLabelu(grid[:, 0], grid[:, 1], gridlabels, opacity=0.5)
    vykresliDataPodleLabelu(data[:, 0], data[:, 1], labels, opacity=1)
    plt.show()
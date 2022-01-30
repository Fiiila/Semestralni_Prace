from matplotlib import pyplot as plt

from Agl_m_v01 import nactiDataDoPole, vykresliDataPodleLabelu
from Bin_deleni import nerovnomerneBinDeleni, rovnomerneBinDeleni
from Kmeans import roztridDoTrid
import numpy as np

def vektorKvantizace(data, pocetTrid):
    '''
    metoda, ktera spusti vektorou kvantizaci
    :param data: vstupni data
    :param pocetTrid: pocet trid
    :return: grid, labels pro grid, labels pro vstupni data, stredni hodnoty jednotlivych trid
    '''

    dataLabels, stredy, cenaTrid, J = nerovnomerneBinDeleni(data, pocetTrid)

    noStep = 50
    xmin, xmax = np.min(data[:, 0]), np.max(data[:, 0])
    xStep = np.abs(xmax - xmin) / noStep
    ymin, ymax = np.min(data[:, 1]), np.max(data[:, 1])
    yStep = np.abs(ymax - ymin) / noStep
    X, Y = np.mgrid[xmin - xStep:xmax + xStep:xStep, ymin - yStep:ymax + yStep:yStep]
    grid = np.stack((X.flatten(), Y.flatten()), -1)

    Ti, J, cena = roztridDoTrid(stredy,grid)

    #olabelovani roztridenych dat
    gridLabels = np.zeros(len(grid),dtype=int)
    for i in range(1,len(Ti)):
        gridLabels[Ti[i]] = i
    return grid, gridLabels, dataLabels, stredy

if __name__ == "__main__":
    nazev = 'data'  # "dataTest2"
    X, Y = nactiDataDoPole(nazev)
    # X, Y = shuffleAndPickData(X,Y,60)
    plt.figure()
    plt.scatter(X, Y)
    plt.show()
    data = np.stack((X, Y), axis=-1)
    grid, gridLabels, labels, stredy = vektorKvantizace(data, 4)
    plt.figure()
    vykresliDataPodleLabelu(grid[:,0], grid[:,1], gridLabels, opacity=0.5)
    vykresliDataPodleLabelu(data[:,0], data[:,1], labels, opacity=1)
    plt.show()


import math

import numpy as np
import matplotlib.pyplot as plt

from Agl_m_v01 import nactiDataDoPole, vykresliDataPodleLabelu


def trainBayes(data, labels):
    '''
    Metoda pro spusteni trenovani klasifikatoru na trenovacich datech od ucitele
    :param data: data od ucitele
    :param labels: labely k odpovizajicim datum
    :return: vraci stredni hodnoty, nalezene kovariancni matice shluku a apriorni ppsti jednotlivych shluku
    '''

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
    '''
    metoda, ktera vytvori labely pro body, ktere jsou metode predany na zaklade obdrzenych stredbich hodnot a kovariancnich matic a apriornich ppsti
    :param body: body, ktere je potreba olabelovat
    :param strHod: stredni hodnoty shluku od ucitele
    :param covMat: kovariancni matice od ucitele
    :param aprPpsti: apriorni ppsti od ucitele
    :return: labely danych bodu v odpovidajicim poradi
    '''
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
    '''
    metoda pro vypocet ppsti, ze bod patri k dane stredni hodnote a covariancni matici resp patri ke shluku temito hodnotami derfinovanym
    :param bod: bod, ktereho ppst chceme zjistit
    :param strHod: stredni hodnota shluku, k nemuz chceme zjistit ppst
    :param covMat: kovariancni matice daneho shluku
    :return: vraci ppst ze bod patri do shluku definovaneho stredni hodnotou a kovariancni matici predane v parametrech
    '''
    n = len(bod)
    diff = bod-strHod
    invCovMat = np.linalg.inv(covMat)
    detCovMat = np.linalg.det(covMat)
    expPart = math.exp(-1/2*diff.T.dot(invCovMat).dot(diff))
    ppst = (1/(math.sqrt(2*math.pi)**n * detCovMat))*expPart
    return ppst

def clasifGrid(body, strHod, covMat, aprPpsti):
    '''
    metoda, ktera vytvori grid bodu v rozsahu bodu z datasetu
    :param body: data, v souvislosti s kterymi budeme vykreslovat grid
    :param strHod: stredni hodnoty jednotlivych shluku
    :param covMat: kovariancni matice definujici jednotlive shluky
    :param aprPpsti: apriorni ppsti jednotlivych shluku
    :return: vytvorene body v gridu a jejich odpovidajici labely
    '''
    noStep = 50
    xmin, xmax = np.min(body[:,0]), np.max(body[:,0])
    xStep = np.abs(xmax-xmin)/noStep
    ymin, ymax = np.min(body[:, 1]), np.max(body[:, 1])
    yStep = np.abs(ymax - ymin) / noStep
    X, Y = np.mgrid[xmin-xStep:xmax+xStep:xStep, ymin-yStep:ymax+yStep:yStep]
    grid = np.stack((X.flatten(), Y.flatten()), -1)

    gridLabel = clasifBayes(grid,strHod,covMat,aprPpsti)
    return grid,gridLabel


def loadLabels(filename):
    '''
    metoda prpo nacteni labelu z textoveho souboru
    :param filename: jmeno souboru popr. cesta k nemu
    :return: vraci labely ve formatu list
    '''
    f = open(filename)
    labels = []
    for line in f:
        labels.append(int(line.strip()))
    f.close()
    return labels

if __name__ == "__main__":
    nazev = 'Data/data600'  # "dataTest2"
    X, Y = nactiDataDoPole(nazev)
    labels = np.array(loadLabels('Data/labels600.txt'))
    #plt.figure()
    #plt.scatter(X, Y)
    #plt.show()
    data = np.stack((X, Y), axis=-1)
    stredniHodnoty, covMat, aprPpsti = trainBayes(data, labels)
    gridPoints,gridLabel = clasifGrid(data,stredniHodnoty,covMat,aprPpsti)
    dataLabels = clasifBayes(data,stredniHodnoty,covMat,aprPpsti)
    plt.figure()
    vykresliDataPodleLabelu(gridPoints[:,0],gridPoints[:,1],gridLabel, opacity=0.3)
    vykresliDataPodleLabelu(data[:, 0], data[:, 1], dataLabels, opacity=1)

    plt.show()

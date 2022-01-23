import sys

import numpy as np
import random
import copy
from matplotlib import pyplot as plt

from Agl_m_v01 import nactiDataDoPole, vykresliDataPodleLabelu
from Bayes_klas import loadLabels
from Klasifikace_NN import makeGrid


def trainKonstPrir(traindata, trainlabels, epochs=10, poDvou=True, beta=0.1):
    pocetShluku = len(np.unique(trainlabels))

    mnoziny = [traindata[trainlabels==i]for i in range(pocetShluku)]
    celkovyVyvojCeny = []
    linDiskrFcns = [[]for i in range(pocetShluku)]
    #hledani parametru pro jednotlive rovnice
    if poDvou:
        for i in range(pocetShluku):
            for j in range(i+1,pocetShluku):
                #vyjmi dve mnoziny, mezi kterymi se bude hledat linearni funkce
                mnozina1 = mnoziny[i]
                mnozina2 = mnoziny[j]
                pocet1 = len(mnozina1)
                pocet2 = len(mnozina2)
                #vytvoreni datasetu pro nasledne trenovani
                datasetlabels = np.ones(pocet1+pocet2, dtype=int)
                datasetlabels[pocet1:pocet1+pocet2] = -1
                dataset = [np.concatenate((mnozina1, mnozina2), axis=0), datasetlabels]
                tempq, prubeh_ceny = train(dataset,epochs, beta)
                linDiskrFcns[i].append(tempq)
                linDiskrFcns[j].append(-tempq)
                celkovyVyvojCeny.append(prubeh_ceny)
    else:
        #hledani parametru pro jednotlive rovnice
        for i in range(pocetShluku):
            #vyjmi dve mnoziny, mezi kterymi se bude hledat linearni funkce
            mnozina1 = mnoziny[i]
            if i ==0:
                j=1
            else: j=0
            mnozina2 = mnoziny[j]
            #hledani lin. diskr fci...nikoliv po dvojicich - nedokonceno
            for k in range(pocetShluku):
                if k==i or k==j:
                    continue
                mnozina2 = np.concatenate((mnozina2,mnoziny[k]))

            pocet1 = len(mnozina1)
            pocet2 = len(mnozina2)
            #vytvoreni datasetu pro nasledne trenovani
            datasetlabels = np.ones(pocet1+pocet2, dtype=int)
            datasetlabels[pocet1:pocet1+pocet2] = -1
            dataset = [np.concatenate((mnozina1, mnozina2), axis=0), datasetlabels]
            tempq, prubeh_ceny = train(dataset,epochs, beta)
            linDiskrFcns[i].append(tempq)
            celkovyVyvojCeny.append(prubeh_ceny)
    return linDiskrFcns, np.sum(celkovyVyvojCeny, axis=0)

def train(dataset, epochs, beta):
    pocetDat = len(dataset[0])
    mixindexes = list(range(pocetDat))
    q = np.zeros(len(dataset[0][0])+1)
    prubeh_ceny = []
    lastdataset = copy.deepcopy(dataset)
    for epoch in range(epochs):
        sys.stdout.write(f'\rTraining epoch {epoch+1}/{epochs} cena: ')  # progress bar
        sys.stdout.flush()
        cena = 0
        #vytvoreni zamichaneho datasetu pro kazdou epochu
        random.shuffle(mixindexes)
        for index in range(pocetDat):
            lastdataset[0][index, :] = dataset[0][mixindexes[index]]
            lastdataset[1][index] = dataset[1][mixindexes[index]]
        #predkladani jednotlivych bodu a hledani krivky
        for i in range(pocetDat):
            tempbod = lastdataset[0][i]
            tempbod = np.insert(tempbod,0,1)
            templabel = lastdataset[1][i]
            if q.T.dot(tempbod) >= 0:
                w = 1
            else:
                w = -1

            if w == templabel:
                #konec
                continue
            else:
                c = beta/(np.dot(tempbod.T,tempbod))
                q = q.T + c*tempbod.T.dot(templabel)
                cena += 1
        prubeh_ceny.append(cena)
        sys.stdout.write(f'\rTraining epoch {epoch+1}/{epochs} prumerna cena: {np.average(prubeh_ceny)}')
    sys.stdout.write('\n')
    return q, prubeh_ceny

def clasify(data, q, poDvou=True):
    datalabels = np.zeros(len(data), dtype=int)
    q = np.asarray(q)
    if poDvou:
        for i in range(len(data)):
            bod = data[i]
            bod = np.insert(bod,0,1)
            label = len(q)
            for j in range(len(q)):
                rozhodnuti = []
                for k in range(len(q[j])):
                    temp = q[j][k].T.dot(bod)
                    if temp >= 0:
                        rozhodnuti.append(True)
                    else:
                        rozhodnuti.append(False)
                if np.all(rozhodnuti):
                    label = j
                    break
            datalabels[i] = label
    else:
        for i in range(len(data)):
            bod = data[i]
            bod = np.insert(bod,0,1)
            label = len(q)
            rozhodnuti = []
            for j in range(len(q)):

                temp = q[j][0].T.dot(bod)
                if temp >= 0:
                    rozhodnuti.append(True)
                    label = j
                else:
                    continue
            if len(rozhodnuti)>1 or len(rozhodnuti)==0:
                label = len(q)
            datalabels[i] = label
    return datalabels





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
    grid = makeGrid(xmin, xmax, ymin, ymax, noStep=50)
    q,vyvojCeny = trainKonstPrir(traindata=data, trainlabels=labels, epochs=20, beta=0.1,poDvou=True)
    q = np.asarray(q)
    print(vyvojCeny)
    gridlabels = clasify(grid, q, poDvou=True)
    '''x = np.linspace(xmin,xmax,2)
    y = []
    for j in range(2):
        for i in range(3):
            y.append((-q[j][i][0]-q[j][i][1]*x)/q[j][i][2])'''
    plt.figure()
    vykresliDataPodleLabelu(grid[:, 0], grid[:, 1], gridlabels, opacity=0.3)
    vykresliDataPodleLabelu(data[:, 0], data[:, 1], labels, opacity=1)
    #for i in range(6):
    #    plt.plot(x,y[i])
    plt.show()
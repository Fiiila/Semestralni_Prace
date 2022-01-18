from Kmeans import K_means
from Agl_m_v01 import nactiDataDoPole, vykresliDataPodleLabelu
import matplotlib.pyplot as plt
import numpy as np

def rovnomerneBinDeleni(data, pocetTrid):

    tridy = []
    tempdata = np.array(data)
    prevTi = np.array(range(len(data)))
    while True:
        Ti, J, u, cenaTrid = K_means(tempdata, 2)

        tempdata1 = tempdata[Ti[0]]
        tridy.append((tempdata1,u[0],cenaTrid[0],prevTi[Ti[0]]))

        tempdata2 = tempdata[Ti[1]]
        tridy.append((tempdata2, u[1], cenaTrid[1],prevTi[Ti[1]]))
        if len(tridy) == pocetTrid:
            break
        tempdata = tridy.pop(0)
        prevTi = tempdata[3]
        tempdata = tempdata[0]
    labels = np.zeros(len(data), dtype=int)
    stredy = []
    for i in range(pocetTrid):
        labels[tridy[i][3]] = i
        stredy.append(tridy[i][1])
    J = sum(cenaTrid)
    return labels, stredy, cenaTrid, J

def nerovnomerneBinDeleni(data, pocetTrid):
    tridy = []
    tempdata = np.array(data)
    prevTi = np.array(range(len(data)))
    while True:
        Ti, J, u, cenaTrid = K_means(tempdata, 2)

        tempdata1 = tempdata[Ti[0]]
        tridy.append((tempdata1, u[0], cenaTrid[0], prevTi[Ti[0]]))

        tempdata2 = tempdata[Ti[1]]
        tridy.append((tempdata2, u[1], cenaTrid[1], prevTi[Ti[1]]))
        if len(tridy) == pocetTrid:
            break
        ceny = np.zeros(len(tridy), dtype=int)
        for j in range(len(tridy)):
            ceny[j] = tridy[j][2]
        tempdata = tridy.pop(np.argmax(ceny))
        prevTi = tempdata[3]
        tempdata = tempdata[0]
    labels = np.zeros(len(data), dtype=int)
    stredy = []
    for i in range(pocetTrid):
        labels[tridy[i][3]] = i
        stredy.append(tridy[i][1])
    J = sum(cenaTrid)
    return labels, stredy, cenaTrid, J

if __name__ =="__main__":
    nazev = 'data'  # "dataTest2"
    X, Y = nactiDataDoPole(nazev)
    # X, Y = shuffleAndPickData(X,Y,60)
    plt.figure()
    plt.scatter(X, Y)
    plt.show()
    data = np.stack((X, Y), axis=-1)
    # vykresliBody(X, Y)
    labels, stredy, cenaTrid, J = nerovnomerneBinDeleni(data, 4)
    plt.figure()
    vykresliDataPodleLabelu(X,Y,labels)
    plt.show()
    # print(Ti)
    #print(J)
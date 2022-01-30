import numpy as np
import copy
import random
from matplotlib import pyplot as plt

from Agl_m_v01 import nactiDataDoPole, vykresliDataPodleLabelu, spoctiVzdalenost, sestavMaticiVzdalenosti
from Bayes_klas import loadLabels
from Kmeans import K_means
from Maximin import pouzijMaximin


def iterativniOptimalizace(data, labels):
    '''
    metoda obsluhujici iterativni optimalizaci vstupnich dat
    :param data: data, ktera chceme optimalizovat (s poradim se nehybe...meni se pouze labely)
    :param labels: labely vstupnich dat, ktera chceme optimalizovat
    :return: nove labely, nove stredni hodnoty, puvodni ceny trid a nopve ceny trid
    '''
    pocet = 0
    cenyTrid, stredniHodnoty = spoctiCenuAStredy(data, labels)
    pocetDat = len(data)
    pocetTrid = len(np.unique(labels))
    #zjisteni cetnosti trid odpovidaji
    cetnost = [len(data[labels==i]) for i in range(pocetTrid)]
    #vytvoreni kopie dat pro nasledne michani vcetne labelu
    tempstredniHodnoty = copy.copy(stredniHodnoty)
    tempcenyTrid = copy.copy(cenyTrid)
    tempdata = copy.deepcopy(data)
    templabels = copy.copy(labels)
    finallabels = copy.copy(labels)
    mixindexes = list(range(pocetDat))
    #cyklus optimalizace probiha dokud nedosahneme nejlepsiho reseni s nejnizsi cenou
    optimalizovat = True
    while optimalizovat:
        #predpokladam, ze se pprerazeni bodu do jine tridy neprovede a optimalizace se tedy ukonci
        optimalizovat = False
        #zamichani dat pred kazdou iteraci
        random.shuffle(mixindexes)
        for index in range(pocetDat):
            tempdata[index] = data[mixindexes[index]]
            tempdata[index] = data[mixindexes[index]]
            templabels[index] = finallabels[mixindexes[index]]
        for i in range(pocetDat):
            tempBod = tempdata[i]
            label_old = templabels[i]
            stred_old = tempstredniHodnoty[label_old]
            cena_old = tempcenyTrid[label_old]
            cetnost_old = cetnost[label_old]
            #pokus prirazeni do vsech ostatnich trid a srovnani cen
            for j in range(pocetTrid):
                # overeni zdali nechceme odebrat bod z mnoziny o jednom prvku nebo priradit prvek do tridy, ze ktereho ho chceme odebrat
                if label_old!=j and cetnost_old>1:
                    #zmena parametru puvodni tridy
                    novy_stred_old = stred_old - (tempBod-stred_old)/(cetnost_old-1)
                    zmena_ceny_old = (cetnost_old/(cetnost_old-1))*spoctiVzdalenost(tempBod, stred_old)
                    nova_cena_old = cena_old - zmena_ceny_old

                    # zmena parametru nove tridy
                    cena_new = tempcenyTrid[j]
                    stred_new = tempstredniHodnoty[j]
                    cetnost_new = cetnost[j]
                    novy_stred_new = stred_new + (tempBod - stred_new)/(cetnost_new + 1)
                    zmena_ceny_new = (cetnost_new / (cetnost_new + 1)) * spoctiVzdalenost(tempBod, stred_new)
                    nova_cena_new = cena_new + zmena_ceny_new

                    #pokud bude prirustek v nove tride mensi nez ubytek v puvodni tride, provedme zmenu
                    if zmena_ceny_old > zmena_ceny_new:
                        pocet += 1
                        finallabels[mixindexes[i]]=j
                        tempstredniHodnoty[label_old] = novy_stred_old
                        tempstredniHodnoty[j] = novy_stred_new
                        tempcenyTrid[label_old] = nova_cena_old
                        tempcenyTrid[j] = nova_cena_new
                        cetnost[label_old] -= 1
                        cetnost[j] += 1
                        optimalizovat = True
                        break
    print(f"Pocet provedenych uprav: {pocet}")
    return finallabels, cenyTrid, tempcenyTrid, tempstredniHodnoty

def vytvorLabel(pocetDat,Ti):
    '''
    metoda pro vytvireni labelu ze znalosti roztrideni indexu jednotlivych bodu do trid
    :param pocetDat: informace o poctu dat pro vytvoreni odpovidajiciho pole labelu
    :param Ti: jednotlive tridy rozdelene do pole poli
    :return: vytvorene labely v odpovidajicim poradi zdrojovych dat
    '''
    labels = np.zeros(pocetDat, dtype=int)
    for i in range(len(Ti)):
        for j in range(len(Ti[i])):
            labels[Ti[i][j]] = i
    return labels

def spoctiCenuAStredy(data, labels):
    '''
    metoda pro ziskani ceny jednotlivych trid a jejich stredni hodnoty
    :param data: vstupni data
    :param labels: labely jednotlivych trid
    :return: pole cen jednotlivych trid, stredni hodnoty odpovidajici cenam trid
    '''
    #labels = np.asarray(labels)
    cena = []
    stredniHodnoty = []
    tridy = [data[labels==i] for i in range(len(np.unique(labels)))]
    for i in range(len(tridy)):
        stredniHodnoty.append(sum(tridy[i])/len(tridy[i]))
        tempcena = 0
        for j in range(len(tridy[i])):
            tempcena += spoctiVzdalenost(tridy[i][j], stredniHodnoty[i])
        cena.append(tempcena)
    return cena, stredniHodnoty

if __name__ == "__main__":
    nazev = "Data/data"
    X, Y = nactiDataDoPole(nazev)
    labels = np.array(loadLabels('Data/labelsbad.txt'))
    plt.figure()
    plt.scatter(X, Y)
    plt.show()
    #matice = sestavMaticiVzdalenosti(X, Y)
    data = np.stack((X, Y), axis=-1)
    #Ti, u = pouzijMaximin(matice, q=0.5, startovniBod=6)
    #templabels = vytvorLabel(len(data), Ti)
    labels[4:1000] = 0
    templabels = copy.copy(labels)
    newlabels,cenyTrid_old, cenyTrid, stredniHodnoty = iterativniOptimalizace(data, templabels)
    print(f"Puvodni cena souctu trid: {sum(cenyTrid_old)}")
    print(f"Nova cena souctu trid: {sum(cenyTrid)}")
    plt.figure()
    plt.subplot(1,2,1)
    vykresliDataPodleLabelu(data[:, 0], data[:, 1], templabels, opacity=1)

    plt.subplot(1,2,2)
    vykresliDataPodleLabelu(data[:, 0], data[:, 1], newlabels, opacity=1)
    plt.show()
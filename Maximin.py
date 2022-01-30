import matplotlib.pyplot as plt

from Agl_m_v01 import sestavMaticiVzdalenosti, nactiDataDoPole

import numpy as np


def najdiNejvzdalenejsiBod(matice, bod):
    '''
    metoda pro nalezeni nejvzdalenejsiho bodu od daneho bodu
    :param matice: matice vzdalenosti
    :param bod: bod, ke kteremu hledam nejvzdalenejsi bod
    :return: vraci index nejvzdalenejsiho bodu
    '''
    u2 = [0, 0]
    for i in range(np.shape(matice)[0]):
        if u2[0] < matice[bod, i]:
            u2 = matice[bod, i], i
    return u2[1]

def najdiNejvzdalenejsiBodOdViceBodu(matice, body):
    '''
    metoda pro nalezeni nejvzdalenejsiho bodu od bodu predanych v poli
    :param data: vstupni data
    :param body: body, ke kterym se ma hledat nejvzdalenejsi
    :return: nejvzdalenejsi bod od zadanych bodu
    '''
    #potrebuji buffer
    buff = [[[0], [0]]for i in range(len(body))] #[[[],[]]]*len(body)
    #i = 0
    for i in range(np.shape(matice)[0]):
        temp = [0] * len(body)
        for j in range(len(body)):
            if buff[j][0][-1] < matice[body[j], i]:
                temp[j] = matice[body[j], i]
                if j ==len(body)-1:
                    for k in range(len(body)):
                        buff[k][0].append(temp[k])
                        buff[k][1].append(i)
                else:
                    continue
                #buff[j][0].append(matice[body[j], i])
                #buff[j][1].append(i)
            else:
                break
    return buff[0][1][-1]


def pouzijMaximin(matice, q=0.5, startovniBod = 0):
    '''
    metoda ridici algoritmus maximin
    :param matice: matice vzdalenosti
    :param q: parametr q
    :param startovniBod: index startovniho bodu
    :return: rozdeleni bodu do trid a stredni hodnoty odpovidajicich shluku
    '''
    #pocatecni inicializace metody maximin
    pocetBodu = np.shape(matice)[0]
    Ti = [[] for i in range(2)]#vytvoreni pole pro zaznam jednotlivych shluku
    u = []  # seznam indexu bodu, ktere byly urceny jako stredni hodnoty
    #pridani prvni stredni hodnoty
    u.append(startovniBod)
    #pridani druhe stredni hodnoty
    u.append(najdiNejvzdalenejsiBodOdViceBodu(matice, [startovniBod]))
    #vymazani prvni hodnoty a nahrazeni novou
    #u[0] = (najdiNejvzdalenejsiBodOdViceBodu(matice, [u[1]]))

    konec = False
    while not konec:
        # rozdeleni do shluku podle minima k jednotlivym strednim hodnotam
        for j in range(pocetBodu):
            if not u.__contains__(j):
                min = [np.inf, 0] # promenna pro nalezeni minima [hodnota minima, index stredni hodnoty ke ktere se priradi]
                for k in range(len(u)):
                    if min[0]>matice[j, u[k]]:
                        min = matice[j, u[k]], k
                Ti[min[1]].append(j)
        # hledani maxima v jednotlivych skupinach
        dmax = [0, [0, 0]]
        for l in range(len(Ti)):
            for m in range(len(Ti[l])):
                if dmax[0]<matice[u[l], Ti[l][m]]:
                    dmax = matice[u[l], Ti[l][m]], [m, l]
        # vypocteni zda je potreba tvorit dalsi novy shluk
        sum = 0
        pocetVazeb = 0
        for n in range(len(u)):
            for o in range(n+1, len(u)):
                sum += matice[u[n], u[o]]
                pocetVazeb += 1
        #print(f'u = {u}\npocet vazeb = {pocetVazeb}')
        qd = q*(sum/pocetVazeb)#(q/pocetVazeb)*sum
        if dmax[0]>qd:
            # vytvor dalsi shluk
            Ti = [[] for p in range(len(Ti)+1)]#vytvoreni pole pro zaznam jednotlivych shluku
            u.append(najdiNejvzdalenejsiBodOdViceBodu(matice, u))
        else:
            # ukonci metodu maximin a vrat vysledek
            konec = True
            for r in range(len(Ti)):
                Ti[r].append(u[r])


    return Ti, u

def vykresliShluky(Ti, X, Y):
    '''
    meotda pro vykresleni bodu podle barev shluku na zaklade indexu jednotlivych shluku zaznamenanych v Ti
    :param Ti:rozdelene body v jednotlivych tridach
    :param X: Xove souradnice vstupnich bodu
    :param Y: Yove souradnice vstupnich bodu
    :return: nevraci nic, jen vykresli do jiz existujiciho figure jednotlive shluky podle rozdeleni v Ti
    '''
    #plt.figure()
    for i in range(len(Ti)):
        shlukX = [0]*len(Ti[i])
        shlukY = [0]*len(Ti[i])
        for j in range(len(Ti[i])):
            shlukX[j] = X[Ti[i][j]]
            shlukY[j] = Y[Ti[i][j]]
        plt.plot(shlukX, shlukY, 'o')
    #plt.show()

def vytvorLabel(pocetDat,Ti):
    '''
    vytvoreni labelovani dat podle rozdelenych bodu v Ti
    :param pocetDat: pocet dat, podle kterho se vytvori vektor labelu
    :param Ti: jednotlive body zarazene do shluku
    :return: vraci pole labelu
    '''
    labels = np.zeros(pocetDat, dtype=int)
    for i in range(len(Ti)):
        for j in range(len(Ti[i])):
            labels[Ti[i][j]] = i
    return labels



if __name__=="__main__":
    nazev = "Data/data"
    X, Y = nactiDataDoPole(nazev)
    matice = sestavMaticiVzdalenosti(X, Y)
    Ti,u = pouzijMaximin(matice, q=0.5, startovniBod=6)
    labels = vytvorLabel(len(X),Ti)
    f = open(f'Data/labelsbad.txt', 'w')
    for i in range(len(labels)):
        f.write(f'{labels[i]}\n')
    f.close()
    print(Ti)
    vykresliShluky(Ti, X, Y)
    plt.show()



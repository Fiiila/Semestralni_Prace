import matplotlib.pyplot as plt
import numpy as np

from Agl_m_v01 import sestavMaticiVzdalenosti, nactiDataDoPole

def hledejRetezMapu(matice, startovniBod = 0):
    pocetDat = np.shape(matice)[0]
    minVzdalenost = np.inf
    pozice = [0, 0]
    retezovaMapa = [[0, 0] for i in range(pocetDat-1)]
    projiteBody = [False for i in range(pocetDat)]
    for i in range(pocetDat-1):#zmenseni poctu prochazeni bodu aby k poslednimu bodu v datasetu nehledal dvojici
        for j in range(0, pocetDat):
            if not projiteBody[j] and matice[startovniBod, j] != 0 and matice[startovniBod, j] < minVzdalenost:
                pozice = startovniBod, j
                minVzdalenost = matice[startovniBod, j]
        retezovaMapa[i][0] = pozice
        retezovaMapa[i][1] = minVzdalenost
        projiteBody[startovniBod] = True
        startovniBod = pozice[1]
        minVzdalenost = np.inf
    return retezovaMapa

def vykresliRetezMapu(retezovaMapa, X, Y):
    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0
    bod1 = 0
    bod2 = 0
    for i in range(len(retezovaMapa)):
        bod1, bod2 = retezovaMapa[i][0]
        x1, y1 = X[bod1], Y[bod1]
        x2, y2 = X[bod2], Y[bod2]
        plt.plot([x1, x2], [y1, y2], 'b')
        plt.plot([x1, x2], [y1, y2], 'ro')
    return

if __name__ == "__main__":
    nazev = "data"#"testData2"
    X, Y = nactiDataDoPole(nazev)
    plt.scatter(X, Y)
    matice = sestavMaticiVzdalenosti(X, Y)
    retMapa = hledejRetezMapu(matice, startovniBod=6)
    #print(retMapa)
    vykresliRetezMapu(retMapa, X, Y)
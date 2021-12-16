import matplotlib.pyplot as plt
import numpy as np

from Agl_m_v01 import sestavMaticiVzdalenosti, nactiDataDoPole

def hledejRetezMapu(matice, startovniBod = 0):
    '''
    Metoda, ktera s pomoci vyhledavani nejmensi vzdalenosti v poskytnutych bodech nalezne retezovou mapu
    Lze ovlivnit odkud metoda bude zacinat hledat retezovou mapu
    :param matice: matice vzdalenosti vsech bodu navzajem
    :param startovniBod: index startovniho bodu v rozmezi 0-posledni index matice
    :return: pole poli, kde vlozena pole maji format [[bodA, bodB],vzdalenost boduA a boduB], ktery muzeme brat jako delku nejkratsi usecky, ktera byla mezi body nalezena
    '''
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
    '''
    Metoda pro vykresleni retezove mapy do jiz existujiciho figure. Vykresli jak body samotne, tak i usecky mezi nimi
    :param retezovaMapa:
    :param X:
    :param Y:
    :return:
    '''
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

def rozdelData(retezovaMapa, threshold):
    '''
    metoda pro rozdeleni dat do jednotlivych trid podle daneho thresholdu vzdalenosti. Rozdeleni probiha tak,
    ze se vytvori pro pocet bodu pole labelu a jednotlive body se olabeluji vzestupne cisly 0,1,2,3...
    :param retezovaMapa: pole retezove mapy obsahujici informace o navazujicich bodech a delkach usecek mezi nimi
    :param threshold: hranice, pri jejiz prekroceni se tvori novy shluk
    :return: vraci pole labelu, pozice v poli oznacuje index bodu ve zdrojovych datech a
    '''
    labels = [0]*(len(retezovaMapa)+1)#vytvoreni pole labelu na zaklade poctu zdrojovych dat
    cisloShluku = 0 #docasny index shluku (po pricteni jednicky lze ziskat celkovy pocet shluku)
    for i in range(len(retezovaMapa)):
        if retezovaMapa[i][1]>threshold:
            cisloShluku += 1
            labels[retezovaMapa[i][0][1]] = cisloShluku
        else:
            labels[retezovaMapa[i][0][1]] = cisloShluku
    return labels, cisloShluku+1

if __name__ == "__main__":
    nazev = "data"#"testData2"
    X, Y = nactiDataDoPole(nazev)
    plt.scatter(X, Y)
    matice = sestavMaticiVzdalenosti(X, Y)
    retMapa = hledejRetezMapu(matice, startovniBod=6)
    #print(retMapa)
    plt.figure()
    vykresliRetezMapu(retMapa, X, Y)
    plt.show()
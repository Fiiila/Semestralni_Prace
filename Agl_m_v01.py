# hledani poctu trid pomoci aglomerativni metody


import datetime
import random
import time

import numpy as np
import matplotlib.pyplot as plt


def nactiDataDoPole(nazevSouboru):
    '''
    nacte data do pole stringu
    vraci dve pole, osa x a y
    co index, to jeden bod v xy plose
    :param nazevSouboru: nazev textoveho souboru, ve kterem se vyskytuji data
    :return: dve pole s hodnotami X a Y
    '''
    f = open(nazevSouboru + '.txt', 'r')
    arrayX = []
    arrayY = []
    for line in f:
        tempX, tempY = line.strip().split()
        arrayX.append(float(tempX))
        arrayY.append(float(tempY))
    return arrayX, arrayY

def spoctiVzdalenost(bod1, bod2):
    '''
    metoda, ktera na zaklade zvolene metriky spocita vzdalenost mezi body ve 2D prostoru
    :param bod1: prvni bod
    :param bod2: druhy bod
    :return: druhou mocnina euklidovske vzdalenosti
    '''
    vzdalenostX = bod1[0] - bod2[0]
    vzdalenostY = bod1[1] - bod2[1]
    vzdalenost = (vzdalenostX * vzdalenostX) + (vzdalenostY * vzdalenostY)
    return vzdalenost


def sestavMaticiVzdalenosti(x, y):
    '''
    Sestavi matici vzdalenosti jednotlivych bodu od sebe
    :param x: x-ove souradnice bodu naskladane v poli
    :param y: y-ove souradnice bodu naskladane v poli
    :return: numpy matice obsahujici informace o vzdalenostech jednotlivych bodu
    '''
    n = len(x)
    matice = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            # vypocteni euklidovske vzdalenosti
            vzdalenost = spoctiVzdalenost([x[i], y[i]], [x[j], y[j]])
            #zakomentovany vypocet vzdalenosti dvou bodu, aby slo jednoduse v metode upravit pripadnou jinou metodu vypoctu
            #vzdalenostX = x[i] - x[j]
            #vzdalenostY = y[i] - y[j]
            #vzdalenost = (vzdalenostX * vzdalenostX) + (vzdalenostY * vzdalenostY)
            matice[i, j] = vzdalenost
            matice[j, i] = vzdalenost
    return matice


def najdiNejmensiVzdalenost(matice):
    '''
    najde nejmensi clen v numpy matici
    :param matice: numpy matice
    :return: nejmensi hodnotu nad hlavni diagonalou a jeji pozici
    '''
    n = len(matice[:, 0])
    nejmensiVzdalenost = np.inf
    nejmensiPozice = [np.inf, np.inf]
    diag = 0 #pomocny index diagonaly, aby metoda prohledavala pouze horni trojuhelnikovou cast matice
    for i in range(n):
        for j in range(diag):
            if matice[i, j] < nejmensiVzdalenost:
                nejmensiPozice = [i, j]
                nejmensiVzdalenost = matice[i, j]

        diag +=1
    return nejmensiVzdalenost, nejmensiPozice


def upravMatici(matice, pozice):
    '''
    Metoda, ktera ma za ukol sloucit dva sloupce(/radky) matice vzdalenosti
    je vsak nutne, aby se jednotlive vzdalenosti porovnavaly a vybralas pouze ta nejmensi. Sloupec/ radek matice
    na vyssi pozici vymaze po procesu porovnavani a prepisovani
    :param matice: matice vzdalenosti
    :param pozice: indexy shluku v matici vzdalenosti, ktere se musi sloucit
    :return: vraci novou aktualizovanou matici se sloucenymi radky/sloupci na zadanych pozicich
    '''
    Xbod = pozice[0]
    Ybod = pozice[1]
    # vytvoreni docasneho vektoru, do ktereho se budou zapisovat minimalni vzdalenosti z obou pozic
    n = np.shape(matice)[0]
    tempVect = np.zeros(n)
    #naplneni docasne matice minimalnimi vzdalenostmi z obou pozic
    for i in range(n):
        if(matice[i,Xbod]<matice[i,Ybod]):
            tempVect[i] = matice[i,Xbod]
        else:
            tempVect[i] = matice[i, Ybod]
    #nalezeni vyssiho indexu pozice, ktery budeme vymazaval
    if(Xbod<Ybod):
        deleteSloupec = Ybod
        rewriteSloupec = Xbod
    else:
        deleteSloupec = Xbod
        rewriteSloupec = Ybod
    tempVect = np.delete(tempVect, deleteSloupec) #vymaz indexu druhe pozice z docasneho pole
    novamatice = np.delete(matice, deleteSloupec, 0) #vymazani radku
    novamatice = np.delete(novamatice, deleteSloupec, 1) #vymazani sloupce
    #prepsani prvni pozice ve zmensene matici docasne vytvorenym polem
    for j in range(n-1):
        novamatice[rewriteSloupec, j] = tempVect[j]
        novamatice[j, rewriteSloupec] = tempVect[j]

    return novamatice


def kresliDendrogram(shluk1, shluk2, hladinaPodobnosti):
    '''
    metoda, ktera na zaklade predanych parametru vykresli jeden krok shlukovani v dendrogramu (pro kompletni dendrogram nutno volat v cyklu)
    :param shluk1: prvni spojovany shluk
    :param shluk2: druhy spojovany shluk
    :param hladinaPodobnosti: hodnota hladiny podobnosti na ktere doslo ke shlukovani
    :return: nevraci nic, pouze vykresluje do jiz existujiciho figure
    '''
    y1 = np.mean(shluk1[0])
    y2 = np.mean(shluk2[0])
    h1 = shluk1[1]
    h2 = shluk2[1]
    plt.plot([h1, hladinaPodobnosti], [y1, y1], 'b')
    plt.plot([h2, hladinaPodobnosti], [y2, y2], 'b')
    plt.plot([hladinaPodobnosti, hladinaPodobnosti], [y1, y2], 'r')
    return

def najdiHladinuH(h):
    '''
    automaticke nalezeni hladiny h a urceni poctu trid
    na zaklade prubehu hladiny h (rozdilu dvou poslednich hladin)
    :param h: hodnoty hladin podobnosti
    :return:
    '''
    max_rozdil_h = 0
    pocet_trid = 0
    for i in range(1, len(h)):
        rozdil_h = h[i] - h[i-1]
        if rozdil_h > max_rozdil_h:
            max_rozdil_h = rozdil_h
            pocet_trid = len(h) - i + 1
    return max_rozdil_h, pocet_trid

def spustShlukovani(dataX, dataY):
    pocetShluku = 1 #rozdelana inicializace, kdy by se shlukovani zastavilo pri potrebnem poctu trid
    # sestaveni matice vzdalenosti
    matice = sestavMaticiVzdalenosti(dataX, dataY)
    # vytvoreni pole s informacemi o shlucich a shlukovych hladinach
    Ti = [([i], 0) for i in range(len(dataX))] #pomocne pole zaznamenavajici postupne shlukovani posledni hodnotu hladiny
    TI = [] #pomocne pole pro zaznamenani prubehu hladin jednotlivych shlukovani
    shluky = [] #pole do ktereho se zaznamenavaji jednotliva shlukovani, pro kazde shlukovani jedno pole s dalsimi dvema poli dvou spojovanych shluku

    while (True):
        if pocetShluku == len(Ti):
            #plt.show() #zobrazeni dendrogramu pri ukonceni shlukovani
            break
        nejmensiVzdalenost, pozice = najdiNejmensiVzdalenost(matice)
        novyShluk = Ti[pozice[0]][0] + Ti[pozice[1]][0]
        # porovnani velikosti indexu, aby nedochazelo ke zcela nahodnemu vymazavani
        if pozice[0] < pozice[1]:
            i1 = pozice[0]
            i2 = pozice[1]
        else:
            i1 = pozice[1]
            i2 = pozice[0]
        kresliDendrogram(Ti[i1], Ti[i2], nejmensiVzdalenost) #vykresleni jednoho kroku shlukovani do dendrogramu
        shluky.append((Ti[i1][0], Ti[i2][0]))
        Ti[i1] = (novyShluk, nejmensiVzdalenost)
        Ti.pop(i2)
        TI.append(nejmensiVzdalenost)
        matice = upravMatici(matice, pozice)
    return Ti, TI, shluky

def vykresliPrubehH(H):
    '''
    metoda pro vykresleni prubehu hladiny podobnosti v prubehu shlukovani
    :param H: pole hodnot hladin podobnosti
    :return: nevraci nic, pouze vykresluje
    '''
    delka = len(H)
    x = list(range(delka))
    y = H
    plt.plot(x, y)
    return

def shuffleAndPickData(X, Y, number):
    '''
    metoda nahodny vyber urciteho poctu bodu z poskytnutych dat
    :param X: hodnoty X poskytnutych dat
    :param Y: hodnoty Y poskytnutych dat
    :param number: pozadovany pocet vyslednych dat
    :return: vraci zadany pocet dat ve formatu dvou poli X,Y
    '''

    seq = list(range(len(X)))#pole obsahujici indexy vstupnich dat
    random.shuffle(seq)#nahodne zamichani indexu
    #podminka pro overeni, zda nebyl pozadovany pocet bodu vyssi nez skutecny
    if number>len(X):
        print(f"Vybrany pocet dat {number} presahuje maximalni moznou volbu {len(X)}/nZvolen maximalni rozsah.")
        number = len(X)
    #inicializace poli pro zapsani zamichanych dat o pozadovane delce
    newX = [0]*number
    newY = [0]*number
    #cyklus pro naplneni novych poli body na nahodne pozici
    for i in range(number):
        newX[i] = X[seq[i]]
        newY[i] = Y[seq[i]]
    return newX, newY

def labelPodleH(shluky, TI, hladH):
    '''
    metodda pro generovani labelu pro jednotlive body na kterych bylo provadeno shlukovani
    :param shluky: pole, ve kterem jsou zaznamenany jednotlive shluky, ktere se spolu shlukovaly
    shluky[poradi shlukovani][0/1 indexy prvniho nebo druheho shluku, ktere se v danem kroku shlukovaly]
    :param TI: hodnoty hladiny podobnosti pro jednotlive kroky shlukovani
    :param hladH: desetinne cislo reprezentujici nalezenou optimalni hladinu H podle ktere se labeluje
    :return: vraci pocet shluku a pole labelu (tzn indexy jednotlivych trid)
    '''
    labels = [0]*(len(shluky[-1][0])+len(shluky[-1][1]))#inicializace prazdneho pole labelu
    labels = np.array(labels)#prevedeni na numpy array
    pocetShluku = 1#promenna, ktera muze slouzit pro kontrolu a validaci poctu shluku
    #cyklus pro porovnavani jednotlivych hladin podobnosti a prirazovani labelu
    #prirazovani labelu probiha na zaklade olabelovani jednoho z puvodnich shluku (jedne vetve)
    for i in range(len(TI)):
        #indexovani TI odzadu, aby jsme nemuseli prochazet a overovat cele pole (jsou tam nejvyssi hondoty)
        if hladH <= TI[-pocetShluku]:
            labels[shluky[-pocetShluku][1]] = pocetShluku
            pocetShluku += 1
        else:
            break
    return pocetShluku, labels

def vykresliDataPodleLabelu(dataX, dataY, labels, opacity=1):
    '''
    vykresli predana data podle labelu jednotlivych bodu
    :param dataX: zdrojova data X
    :param dataY: zdrojova data Y
    :param labels: labely jendotlivych bodu (index v poli labelu odpovida indexu v datech X a Y)
    :return: nevraci nic, pouze vyplotuje data podle labelu do jiz existujiciho figure
    '''
    pocetShluku = len(np.unique(labels))#zjisteni poctu shluku z poctu rozdilnych oznaceni trid v poli labels.txt
    #inicializace hodnot x a y pro jednotlive tridy pro jednoduche vykresleni
    colorpalette = ['tab:blue','tab:orange','tab:green','tab:red','tab:purple','tab:brown','tab:pink','tab:gray','tab:olive','tab:cyan']
    x = [[] for i in range(pocetShluku)]
    y = [[] for i in range(pocetShluku)]
    #cyklus pro nacteni hodnot dat do poli odpovidajicich trid
    for j in range(len(labels)):
        x[labels[j]].append(dataX[j])
        y[labels[j]].append(dataY[j])
    #cyklus pro vykresleni shluku
    for i in range(pocetShluku):
        plt.plot(x[i], y[i], 'o', alpha=opacity, color=colorpalette[i])
    return


if __name__ == '__main__':
    '''NUTNE DODELAT KOMENTARE U HLAVNI SHLUKOVACI METODY'''
    nazev = 'data'
    pocetBodu = 60

    #nacteni dat do dvou poli
    dataX, dataY = nactiDataDoPole(nazev)
    plt.scatter(dataX, dataY)
    dataX, dataY = shuffleAndPickData(dataX, dataY, pocetBodu)
    plt.scatter(dataX,dataY)
    start = time.time()
    plt.figure()
    Ti, TI, shluky = spustShlukovani(dataX, dataY)
    end = time.time()
    print(f"shlukovani trvalo {end-start} s")
    plt.figure()
    vykresliPrubehH(TI)
    #plt.show()
    H, _ = najdiHladinuH(TI)
    pocetShluku, labels = labelPodleH(shluky, TI, H)
    f = open('Data/labels.txt', 'w')
    for i in labels:
        f.write(str(i)+'\n')

    f.close

    plt.figure()
    vykresliDataPodleLabelu(dataX, dataY, labels)
    plt.show()
    print('hotovo')


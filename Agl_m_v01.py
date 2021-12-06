# hledani poctu trid pomoci aglomerativni metody


import datetime
import numpy as np
import matplotlib.pyplot as plt

def vykresliShluky(Ti, X, Y):
    plt.figure()
    for i in range(len(Ti)):
        shlukX = [0]*len(Ti[i])
        shlukY = [0]*len(Ti[i])
        for j in range(len(Ti[i])):
            shlukX[j] = X[Ti[i][j]]
            shlukY[j] = Y[Ti[i][j]]
        plt.plot(shlukX, shlukY, 'o')
    plt.show()


def vykresliBody(x, y):
    plt.figure()
    plt.scatter(x, y)
    plt.show()
    return

def nactiDataDoPole(nazevSouboru):
    '''
    nacte data do pole stringu
    vraci dve pole, osa x a y
    co index, to jeden bod v xy plose
    :param nazevSouboru: nazev textoveho souboru, ve kterem se vyskytuji data
    :return: dve pole s hodnotami X a Y
    '''
    f = open('D:\Filip\Documents\Personal\School\FAV\Zima_2020\ZSUR\Semestralni_Prace\Data\\' + nazevSouboru + '.txt', 'r')
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
    Sestavi pocatecni matici vzdalenosti k nactenym datum

    :type x: int
    :param x: x-ove souradnice bodu naskladane v poli
    :type   y: int
    :param y: y-ove souradnice bodu naskladane v poli
    :return: numpy matice obsahujici informace o vzdalenostech jednotlivych bodu
    '''
    n = len(x)
    matice = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            # vypocteni euklidovske vzdalenosti
            vzdalenost = spoctiVzdalenost([x[i], y[i]], [x[j], y[j]])
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
    diag = 0
    #tempprvekmatice = 0
    for i in range(n):
        for j in range(diag):
            #tempprvekmatice = matice[i, j]
            if matice[i, j] < nejmensiVzdalenost:
                nejmensiPozice = [i, j]
                nejmensiVzdalenost = matice[i, j]

        diag +=1
    # for i in range(n):
    #     for j in range(i + 1, n):
    #         tempCislo = matice[i, j]
    #         if tempCislo == 0:
    #             continue
    #         elif tempCislo < nejmensiVzdalenost:
    #             nejmensiVzdalenost = tempCislo
    #             nejmensiPozice[0], nejmensiPozice[1] = i, j
    #             continue
    return nejmensiVzdalenost, nejmensiPozice


def upravMatici(matice, pozice):
    Xbod = pozice[0]
    Ybod = pozice[1]
    # vytvoreni docasneho vektoru, ktery se pak zapise misto obou
    n = np.shape(matice)[0]
    tempVect = np.zeros(n)
    for i in range(n):
        if(matice[i,Xbod]<matice[i,Ybod]):
            tempVect[i] = matice[i,Xbod]
        else:
            tempVect[i] = matice[i, Ybod]
    if(Xbod<Ybod):
        deleteSloupec = Ybod
        rewriteSloupec = Xbod
    else:
        deleteSloupec = Xbod
        rewriteSloupec = Ybod
    tempVect = np.delete(tempVect, deleteSloupec)
    novamatice = np.delete(matice, deleteSloupec, 0) #vymazani radku
    novamatice = np.delete(novamatice, deleteSloupec, 1) #vymazani sloupce
    for j in range(n-1):
        novamatice[rewriteSloupec, j] = tempVect[j]
        novamatice[j, rewriteSloupec] = tempVect[j]

    return novamatice



def shlukovaHladina(X,Y,pocetShluku = 1):
    '''
    Aglomerativni metoda (shlukove hladiny) ktera rozdeli vstupni data do shluku podle euklidovske vzdalenosti 2D bodu

    :param X: x-ove souradnice bodu v poli
    :param Y: y-ove souradnice bodu v poli
    :param pocetShluku: pocet trid do kterych se maji vstupni data rozdelit
    :return:
    '''
    n = len(X)
    pocMaticeVzdalenosti = sestavMaticiVzdalenosti(X, Y)

def kresliDendrogram(shluk1, shluk2, hladinaPodobnosti):
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
    na zaklade prubehu hladiny h
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
    return pocet_trid, max_rozdil_h


if __name__ == '__main__':
    '''chybi dodelat automaticke hledani shlukovych hladin a vykreslovani dat do nejruznejsich podob'''
    nazev = 'testData'
    #nazev = 'data_600'
    programStart=datetime.datetime.now()


    print("Nacteni dat ze souboru.")
    start = datetime.datetime.now()
    #nacteni dat do dvou poli
    dataX, dataY = nactiDataDoPole(nazev)
    end = datetime.datetime.now()
    elapsed = end - start
    print('Nacteni dat ze souboru do polí: ', elapsed)

    # vykresleni importovanych 2D dat pro lepsi orientaci
    '''plt.plot(dataX, dataY, 'o')
    plt.title('Importovana data')
    plt.xlabel('osa x')
    plt.ylabel('osa y')
    plt.show()'''


    #sestaveni matice vzdalenosti
    print("Sestavení matice vzdalenosti.")
    start = datetime.datetime.now()
    matice = sestavMaticiVzdalenosti(dataX, dataY)
    end = datetime.datetime.now()
    elapsed = end - start
    print('Sestavení matice vzdalenosti: ', elapsed)
    #vytvoreni pole s informacemi o shlucich a shlukovych hladinach
    Ti = [([i], 0) for i in range(len(dataX))]
    TI = [ 0 for i in range(len(dataX)-1)]

    #print(matice)
    #print(dataX)
    #elapsednejmensi = datetime.timedelta.min
    #elapsedupravmatici = datetime.timedelta.min
    plt.figure()
    pocitadlo = 0
    while(True):
        #start = datetime.datetime.now()
        nejmensiVzdalenost, pozice = najdiNejmensiVzdalenost(matice)
        novyShluk = Ti[pozice[0]][0]+Ti[pozice[1]][0]
        #porovnani velikosti indexu, aby nedochazelo ke zcela nahodnemu vymazavani
        if pozice[0]<pozice[1]:
            i1 = pozice[0]
            i2 = pozice[1]
        else:
            i1 = pozice[1]
            i2 = pozice[0]
        kresliDendrogram(Ti[i1], Ti[i2], nejmensiVzdalenost)
        Ti[i1] = (novyShluk, nejmensiVzdalenost)
        Ti.pop(i2)
        TI[pocitadlo] = nejmensiVzdalenost
        #print(TI)

        #end = datetime.datetime.now()
        #elapsed = end - start
        #elapsednejmensi += elapsed
        #print(f"nalezeni nejmensi vzdalenosti: {elapsed}")
        #print(nejmensi)
        #start = datetime.datetime.now()
        matice = upravMatici(matice, pozice)
        #end = datetime.datetime.now()
        #elapsed = end - start
        #elapsedupravmatici += elapsed
        #print(f"upraveni matice: {elapsed}")
        #print(matice)
        if (np.shape(matice)[0] == 1):
            programEnd = datetime.datetime.now()
            programElapsed = programEnd - programStart
            print(najdiHladinuH(TI))
            plt.show()
            break
        pocitadlo += 1
    #print(f"nalezeni nejmensi vzdalenosti: {elapsednejmensi}")
    #print(f"upraveni matice: {elapsedupravmatici}")
    #nalezeni hladin
    # start = datetime.datetime.now()
    # hladinaPodobnosti, body = najdiNejmensiVzdalenost(matice)
    # end = datetime.datetime.now()
    # elapsed = end - start
    # print(hladinaPodobnosti, body)
    # print(elapsed)

    # start = datetime.datetime.now()
    # matice = upravMatici(matice, body)
    # end = datetime.datetime.now()
    # elapsed = end - start
    # print(matice)
    # print(elapsed)
    '''
    #zapsani hladin podobnosti a bodu do souboru
    output='output.txt'
    f = open(output, 'w')
    start = datetime.datetime.now()
    hladinaPodobnosti, body = najdiNejmensiVzdalenost(matice)
    f.write(str(hladinaPodobnosti)+','+str(body[0])+','+str(body[1]))
    predchoziHladina = hladinaPodobnosti
    end = datetime.datetime.now()
    elapsed = end - start
    print('Nalezeni nejmensi vzdalenosti: ',elapsed)
    start = datetime.datetime.now()
    matice = upravMatici(matice, body)
    end = datetime.datetime.now()
    elapsed = end - start
    print('Snizeni dimenze matice: ',elapsed)
    #print(matice)
    for i in range(len(dataX)-2):
        start = datetime.datetime.now()
        hladinaPodobnosti, body = najdiNejmensiVzdalenost(matice)
        if hladinaPodobnosti==predchoziHladina:
            f.write(str(body[0])+','+str(body[1]))
        else:
            f.write('\n'+str(hladinaPodobnosti)+','+str(body[0])+','+str(body[1]))
        matice = upravMatici(matice, body)
        end = datetime.datetime.now()
        elapsed = end - start
        print('Cas pro snizeni dimenze v poradi: ',i+1,)
        print(elapsed,'\n')
    
    f.close()'''

    print('Celkovy cas vypoctu: ', programElapsed)

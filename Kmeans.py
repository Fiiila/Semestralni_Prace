#ve skriptech na strane 135
import random

import numpy as np

from Agl_m_v01 import spoctiVzdalenost, nactiDataDoPole, shuffleAndPickData
from Maximin import vykresliShluky
from random import randint
import matplotlib.pyplot as plt
random.seed(2)#nastaveni seedu...1-dobry vysledek 2-spatny vysledek

def najdiNejvzdalenejsiBodOdViceBodu(data, body):
    #potrebuji buffer
    buff = [[[0], [0]]for i in range(len(body))] #[[[],[]]]*len(body)
    #i = 0
    '''
    for i in range(len(data)):
        temp = [0] * len(body)
        for j in range(len(body)):
            cislo = spoctiVzdalenost(data[i], body[j])
            if buff[j][0][-1] < cislo:
                temp[j] = cislo
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
                '''
    prevsum = 0
    for i in range(len(data)):
        temp = [0] * len(body)
        sum = 1
        for j in range(len(body)):
            cislo = spoctiVzdalenost(data[i], body[j])
            temp[j] = cislo
            sum *=cislo


        if prevsum < sum:
            for k in range(len(body)):
                buff[k][0].append(temp[k])
                buff[k][1].append(i)
                prevsum = sum
        else:
            continue
                # buff[j][0].append(matice[body[j], i])
                # buff[j][1].append(i)
    return data[buff[0][1][-1]]

def roztridDoTrid(stredniHodnoty, data):
    J = 0
    cenaTrid = np.zeros(len(stredniHodnoty))
    Ti = [[]for i in range(len(stredniHodnoty))] #vysledne tridy
    for i in range(len(data)):
        min = [np.inf, 0] # promenna pro nalezeni minima [hodnota minima, index stredni hodnoty ke ktere se priradi]
        for j in range(len(stredniHodnoty)):
            tempVzdalenost = spoctiVzdalenost(data[i], stredniHodnoty[j])
            if min[0] > tempVzdalenost:
                min = tempVzdalenost, j
        Ti[min[1]].append(i)
        J += min[0]
        cenaTrid[min[1]] += min[0]
    return Ti, J, cenaTrid

def upravStredniHodnoty(Ti, stredniHodnoty, data):
    for i in range(len(Ti)):
        tempStrHod = [0, 0]
        for j in range(len(Ti[i])):
            tempStrHod[0] += data[Ti[i][j]][0]
            tempStrHod[1] += data[Ti[i][j]][1]
        tempStrHod[0] = tempStrHod[0]/len(Ti[i])
        tempStrHod[1] = tempStrHod[1]/len(Ti[i])
        stredniHodnoty[i] = tempStrHod
    return stredniHodnoty

def K_means(data, pocetTrid):
    #pocatecni inicializace parametru
    Ti = [[]for i in range(pocetTrid)] #vysledne tridy
    u = [[]for i in range(pocetTrid)] #vektory mi
    J = [] #ukazatel kvality

    #nalezeni nejvzdalenejsich startovnich bodu v datech
    #u = [[]]*pocetTrid #pocatecni definice poctu strednich hodnot
    rCislo = randint(0, len(data)-1) #nahodny index startovaciho cisla z dat
    tempBod = data[rCislo] #nahodne cislo
    #print(f"prvni docasny bod {tempBod}")
    tempBod = najdiNejvzdalenejsiBodOdViceBodu(data, [tempBod]) #nalezeni nejvzdalenejsiho cisla k nahodne zvolenemu cislu
    #print(f"druhy docasny bod {tempBod}")
    u[0] = tempBod #prirazeni prvni stredni hodnoty nejvzdalenejsimu cislu vzhledem k nahodne vybranemu startovacimu cislu
    #cyklus pro vyhledani zbylych nejvzdalenejsich strednich hodnot
    #print(f"zapsany bod {u}")
    for i in range(pocetTrid-1):
        u[i+1] = najdiNejvzdalenejsiBodOdViceBodu(data, u[0:i+1])
    Ti, ukazatelKvality, cenaTrid = roztridDoTrid(u, data)
    J.append(ukazatelKvality)
    konec = True
    while(konec):
        minuleStartovaciBody = np.copy(u)
        u = np.asarray(upravStredniHodnoty(Ti, u, data))
        Ti, ukazatelKvality, cenaTrid = roztridDoTrid(u, data)
        J.append(ukazatelKvality)
        #if np.sum([dist(minuleStartovaciBody[i], u[i]) for i in range(len(u))]) <= 1e-3:
        if (u == minuleStartovaciBody).all():
            konec = False
    return Ti, J, u, cenaTrid

def dist(a,b):
    a = np.array(a)
    b = np.array(b)
    diff = a - b
    return np.dot(diff, diff.T)


if __name__=="__main__":
    nazev = 'data'#"dataTest2"
    X, Y = nactiDataDoPole(nazev)
    X, Y = shuffleAndPickData(X,Y,600)
    plt.figure()
    plt.scatter(X,Y)
    plt.show()
    data = np.stack((X,Y),axis=-1)
    #vykresliBody(X, Y)
    Ti, J, u, cenaTrid = K_means(data, 4)
    print(Ti)
    print(J)
    #print('mi', u)
    vykresliShluky(Ti, X, Y)
    plt.plot([u[0][0],u[1][0],u[2][0],u[3][0]],[u[0][1],u[1][1],u[2][1],u[3][1]],'yo')
    plt.show()





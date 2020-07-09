import numpy as np
from scipy.stats import chi2
from scipy.stats import binom
from random import random
from collections import Counter

class PearsonTest():
    def __init__(self,sample,pi,k,frequencies=True):
        self.sample = sample
        self.pi = pi
        self.k = k
        if frequencies:
            self.n_i = sample
            self.n = sum(sample)
        else:    
            freq = Counter(sample)
            # We would like to order these frequencies
            self.n_i = list({k: freq[k] for k in sorted(freq)}.values())
            self.n = len(sample)
        self.t = self.statistic(self.k,self.n,self.pi,self.n_i)
    
    def statistic(self,k,n,pi,n_i):
        t = 0
        for i in range(k):
            npi = n*pi[i]
            t += ((n_i[i] - npi)**2)/npi
        return t
    
    def p_value_chi2(self):
        return 1 - chi2.cdf(self.t , self.k -1)
    
    def sim_n_i(self):
        n = self.n
        pi = self.pi
        k = self.k
        Nis = []
        p = 1
        N = binom.rvs(n,pi[0])
        Nis.append(N)
        for i in range(1,k):
            p -=pi[i-1]
            Ni = binom.rvs(n-N,pi[i]/p)
            N += Ni
            Nis.append(Ni)
        return Nis

    
    def p_value_sim(self,nSim):
        obs_frec = [self.sim_n_i() for _ in range(nSim)]
        p = 0
        for n_i in obs_frec:
            t_sim = self.statistic(self.k,self.n,self.pi,n_i)
            if t_sim >= self.t:
                p += 1
        return p/nSim
        
def generar_Ni(pi,k,n):
    Nis = []
    p = 1
    N = binom.rvs(n,pi[0])
    Nis.append(N)
    for i in range(1,k):
        p -=pi[i-1]
        Ni = binom.rvs(n-N,pi[i]/p)
        N += Ni
        Nis.append(Ni)
    return Nis

def estadistico_t(n, Ni, pi, k):
    """
    Calcula el estadistico T (chi2)
    n : tamaño de la muestra
    Ni : lista con las frecuencias obs
    pi : lista con las probabilidades asociadas
    k : cantidad de datos unicos (?)
    """
    res = 0
    for i in range(k):
        npi = n*pi[i]
        res += ((Ni[i] - npi)**2) / npi
    return res

def ej1():
    n = 564
    nsim = 1000
    Ni = [141, 291, 132]
    pi = [0.25, 0.5, 0.25]

    # Parte 1 - aproximación del p-valor con chi2
    T = estadistico_t(n, Ni, pi, 3)
    print('Estadistico T: ', T)
    print('p-valor con chi2: ', 1 - chi2.cdf(T, 2))

    fo = [generar_Ni(pi,3,n) for _ in range(nsim)] #frecuencia observada de c/muestra
    exitos = 0
    for muestra in fo:
        dsim = estadistico_t(n, muestra, pi, 3)
        if dsim >= T:
            exitos += 1
    exitos /= nsim
    print('p-valor con simulación: ', exitos)


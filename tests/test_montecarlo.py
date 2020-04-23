import pytest
from math import exp
import monteCarlo.monteCarlo as monteCarlo
from scipy.integrate import quad
import numpy as np


def errorMargin(actualValue,expectedValue,range):
    return -range <= actualValue - expectedValue <= range


def test_monteCarlo01():
    f = (lambda x: exp(x+x**2))
    nSim = 1000
    monteCarloEstimation = monteCarlo.monteCarlo01(f,nSim)
    realValue = quad(f,0,1)[0]
    assert errorMargin(monteCarloEstimation,realValue,0.2)

def test_monteCarloab():
    f = (lambda x: exp(x+x**2))
    nSim = 1000
    monteCarloEstimation = monteCarlo.monteCarloab(f,-1,1,nSim)
    realValue = quad(f,-1,1)[0]
    assert errorMargin(monteCarloEstimation,realValue,0.5)

def test_monteCarloInfinite0():
    f = lambda u: (u*(1+u**2)**(-2))
    nSim = 1000
    monteCarloEstimation = monteCarlo.monteCarloInfinite0(f,nSim)
    realValue = quad(f,-np.inf,0)[0]
    assert errorMargin(monteCarloEstimation,realValue,0.5)

def test_monteCarlo0Infinite():
    f = lambda u: (u*(1+u**2)**(-2))
    nSim = 1000
    monteCarloEstimation = monteCarlo.monteCarlo0Infinite(f,nSim)
    realValue = quad(f,0,np.inf)[0]
    assert errorMargin(monteCarloEstimation,realValue,0.5)

def test_monteCarloInfInfEvenFun():
    f = lambda u: (u*(1+u**2)**(-2))
    nSim = 1000
    monteCarloEstimation = monteCarlo.monteCarloInfInf(f,nSim)
    realValue = quad(f,-np.inf,np.inf)[0]
    assert errorMargin(monteCarloEstimation,realValue,0.5)

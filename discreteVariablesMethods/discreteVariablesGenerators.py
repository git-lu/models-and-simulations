from random import random
from collections import defaultdict
from math import exp , log

class RejectionMethod():
    '''
    Implements the rejection method for generating a random variable with probability
    distribution X, from a support funcion Y, asuming we have a known random generator
    for function Y.
    Y must be a mass probability function such that:
    - P(X = xj) > 0 then P(Y = xj) > 0 for all xj in X range
    - A positive constant c exists such that P(X=xj)/P(Y=xj) <= c for all xj 
    where P(X=xj) > 0.

    You can generate one of the default distributions or a "custom" one where:
    X_function: mass probability function of the variable we wish to generate
    Y_function: support function
    Y_generator: generator of the support function Y. Generates a random Y with distribution
    probability Y_function
    n_values: Number of elements in X domain. This is to calculate C.
    c: c constant if known.
    '''
    def __init__(
        self, X_generator=None, Y_generator=None,
        X_function=None, Y_function=None,c=None,n_values=None):

        self.x_gen = X_generator
        self.y_gen = Y_generator

        self.x_func = X_function
        self.y_func = Y_function

        self.n = n_values
        self.c = c

        if c is None and self.n:
            self.c = self.__calculate_c__(self.n)

    def generate(self, iterations):
        '''
        Generates {iterations} random ints from distribution and
        stores the generated values in a dictionary
        '''

        values = defaultdict(int)

        for _ in range(iterations):
            y_value = self.y_gen()
            x_value = self.x_gen()

            while x_value > self.x_func(y_value) / (self.c * self.y_func(y_value)):
                y_value = self.y_gen()
                x_value = self.x_gen()
            values[y_value] += 1
        return values
            
    def generateInt(self):
        '''
        Generates a random int
        '''
        value = 0
        c = self.c
        y = self.y_gen()
        u = random()
        while u > self.x_func(y) / (c * self.y_func(y)):
            u = random()
            y = self.y_gen()
        value = y
        return value

    def __calculate_c__(self,n):
        c = 1
        for i in range(n):
            if (self.x_func(i)/self.y_func(i)) >= c:
                c = self.x_func(i)/self.y_func(i)
        return c + 0.1




class InverseTransform():
    '''
    Given a distribution of probability p_i generates a random number with that
    probability distribution
    '''
    def __init__(self, p_i=None):
        if not (isinstance(p_i, dict) or p_i is None):
            raise ValueError("Weights must be a dict or a subclass of dict")
        # Sort the weights for improved efficency
        if isinstance(p_i, dict):
            if sum(p_i.values()) != 1:
                raise ValueError("The given dict does not represent a probability function")            
            self.p_i = sorted(p_i.items(), key=lambda x: x[1], reverse=True)

    def generate(self, iterations):
        '''
        Generates a dictionary with the count of values generated in a 
        given number of iterations
        '''
        values = defaultdict(int)

        for _ in range(iterations):
            u = random()
            accum = 0
            for key, value in self.p_i:
                accum += value
                if u <= accum:
                    values[key] += 1
                    break
        return values

    def generateInt(self):
        '''
        Generates a random int with the probability distribution given
        '''
        u = random()
        accum = 0
        generatedValue = 0
        # We initialize the value with the first element of the
        # sorted probability array
        for v,prob in self.p_i:
            accum += prob
            if u <= accum:
                generatedValue = v
                break
        return generatedValue 
               
    def generateBinomialInt(self,n,p):
        '''
        Inverse transformation method using p < 0.5 
        '''
        U = random()
        i = 0
        reversedP = False
        if p > 0.5:
            p = 1-p
            reversedP = True
        c = p / (1-p)
        prob = (1-p) ** n
        F = prob
        while U >= F:
            prob = c * (n-i) / (i+1) * prob
            F= F + prob 
            i = i + 1
        res = i
        if reversedP:
            res = n - i
        return res
    
    def generateNaivePoisson(self,lamda):
        '''
        Generates a random int with poisson distribution. 
        '''
        U = random() 
        value = 0 
        p = exp(-lamda)
        F = p
        while U >= F:
            value += 1        
            p *=lamda / value
            F = F + p
        return value

    def generatePoisson(self,lamda):
        '''
        Generates a random int with poisson distribution with
        parameter lamda.
        Improves implementation that orders the probability
        distribution
        '''
        lamdaInt = int(lamda)
        p = exp(-lamda)
        F = p
        ## We calculate F(lamda), that is the larger probability value.
        for i in range(1,lamdaInt+1):
            p *= lamda / i
            F += p
        u=random()
        value = lamdaInt
        # We generate a random number, as always
        if u >= F: 
            # If u >= F , it means we have to "look" for a number that has greater
            # probability of occurring
            while u > F:
                value += 1
                p *= lamda/value
                F += p
            return value
        else:
            # If u< F, we look for a number that hast lesser probability of ocurring
            while u < F:
                F -= p
                p *= value / lamda
                value -= 1
            return value + 1    

    def generateGeometricInt(self,p):
        '''
        Generates a geometric random int with
        geometric ditribution with success probability p
        '''
        u = 1-random()
        return int(log(u)/log(1-p))+1



class CompositionMethod():
    '''
    Composition method allows us to generate a random variable X with 
    probability mass function  
    P(X=j) = alpha*p_j + (1-alpha)*q_j with j = 0,1,..., and 0 < alpha < 1
    ''' 
    def __init__(self,X_generator,Y_generator,alpha):
        if alpha < 0 or alpha > 1:
            raise ValueError("Alpha must be a number between 0 and 1")
        self.x_gen = X_generator
        self.y_gen = Y_generator
        self.alpha = alpha    


    def generateInt(self):
        '''
        Generate random int
        '''
        u = random()
        generatedValue = 0
        if u < self.alpha:
            generatedValue = self.x_gen()
        else:
            generatedValue = self.y_gen()
        return generatedValue


class RiskRateMethod():
    '''
    Given a mass probability function f, risk rate method generates a discrete
    random variable with distribution f.
    ''' 
    def __init__(self,func):
        self.func = func

    def __calculateRiskRate__(self,n):
        ''' 
        Given a mass probability function f, the risk method for a value n
        is defined as follows:
        riskRate(n) = P(X=n | X>n-1) = f(n)/(1-acummulatedMassProbability(n-1))
        '''
        f = self.func
        acumDist = sum(f(i) for i in range(1,n-1)) 
        riskRate = f(n)/(1-acumDist)
        return riskRate

    def generateInt(self):
        '''
        Generates random int
        '''
        u = random()
        f = self.func
        generatedValue = 1
        riskRate = f(1)
        while u > riskRate:
            generatedValue += 1
            riskRate = self.__calculateRiskRate__(generatedValue)
        return generatedValue
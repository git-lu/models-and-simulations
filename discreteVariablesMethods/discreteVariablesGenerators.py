from random import random
from collections import defaultdict
from math import exp

class RejectionMethod():
    ''' Implements the rejection method for generating a random variable with probability
    distribution X. '''
    def __init__(
        self, X_generator=None, Y_generator=None,
        X_function=None, Y_function=None,c=None,n_values=None):

        self.x_gen = X_generator
        self.y_gen = Y_generator

        self.x_func = X_function
        self.y_func = Y_function

        self.n = n_values
        self.c = c

        if c is None:
            self.c = self.calculate_c(self.n)

    def generateFromFun(self, iterations):
        values = defaultdict(int)

        for _ in range(iterations):
            y_value = self.y_gen()
            x_value = self.x_gen()

            while x_value > self.x_func(y_value) / (self.c * self.y_func(y_value)):
                y_value = self.y_gen()
                x_value = self.x_gen()
            values[y_value] += 1
        return values

    def generate(self,iterations):
        if self.x_func:
            for _ in range(iterations):
                self.generateIntFromFun()


    def generateInt(self):
        value = 0
        if self.x_func:
            value = self.generateIntFromFun()
        return value
            
    def generateIntFromFun(self):
        value = 0
        c = self.c
        y = self.y_gen()
        u = random()
        while u < self.x_func(y) / (c * self.y_func(y)):
            u = random()
            value = y
        return value

    def calculate_c(self,n):
        c = 1
        for i in range(n):
            if (self.x_func(i)/self.y_func(i)) >= c:
                c = self.x_func(i)/self.y_func(i)
        return c + 0.01




class InverseTransform():
    ''' Given a distribution of probability p_i generates a random number with that
    probability distribution'''
    def __init__(self, p_i=None):
        if not (isinstance(p_i, dict) or p_i is None):
            raise ValueError("Weights must be a dict or a subclass of dict")
        # Sort the weights for improved efficency
        if isinstance(p_i, dict):
            self.p_i = sorted(p_i.items(), key=lambda x: x[1], reverse=True)

    def generate(self, iterations):
        ''' Generates a dictionary with the count of values generated in a 
        given number of iterations'''
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
        '''Generates a random int with the probability distribution given'''
        u = random()
        accum = 0
        value = 0
        p_i = self.p_i
        for key,value in p_i:
            accum += value
            if u <= accum:
                value = key
            break
        return value 
               
    def generateBinomialInt(self,n,p):
        '''Inverse transformation method using p < 0.5 '''
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
        U = random() 
        value = 0 
        p = exp(-lamda)
        F = p
        while U >= F:
            value += 1        
            p *=lamda / value
            F = F + p
        return value

    def generatePoisson(self,L):
        I = int(L)
        p = exp(-L)
        F = p
        ## Cálculo de F(I)
        for i in range(1,I+1):
            p *= L / i
            F += p
        u=random()
        if u>=F: #recorre I, I+1, I+2, ...
            while u>F:
                I += 1
                p *= L/I
                F += p
            return I
        else:
            while u < F: #recorre I-1, I-2, ...
                F -= p
                p *= I / L
                I -= 1
            return I + 1    


class CompositionMethod():
    def __init__(self):
        pass
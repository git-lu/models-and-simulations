from random import random
from collections import defaultdict
from math import exp , log

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
            if sum(p_i.values()) != 1:
                raise ValueError("The given array does not represent a probability function")            
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

    def generatePoisson(self,lamda):
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
        u = 1-random()
        return int(log(u)/log(1-p))+1



class CompositionMethod():
    ''' Composition method allows us to generate a random variable X with 
    probability mass function  
    P(X=j) = alpha*p_j + (1-alpha)*q_j with j = 0,1,..., and 0 < alpha < 1''' 
    def __init__(self,X_generator,Y_generator,alpha):
        if alpha < 0 or alpha > 1:
            raise ValueError("Alpha must be a number between 0 and 1")
        self.x_gen = X_generator
        self.y_gen = Y_generator
        self.alpha = alpha    


    def generateInt(self):
        u = random()
        generatedValue = 0
        if u < self.alpha:
            generatedValue = self.x_gen()
        else:
            generatedValue = self.y_gen()
        return generatedValue


from random import random
from collections import defaultdict

def generateRandomPermutation(a):
    ''' Returns a random permutation of array a'''
    N = len(a)
    for j in range(N-1,0,-1):
        index = int((j+1)*random())
        a[j] , a[index] = a[index], a[j]
    return a

class RejectionMethod():
    ''' Implements the rejection method for generating a random variable with probability
    distribution X'''
    def __init__(self, X_generator, Y_generator, X_function, Y_function, c=None):
        self.x_gen = X_generator
        self.y_gen = Y_generator

        self.x_func = X_function
        self.y_func = Y_function
        self.c = c

        if c is None:
            self.c = self.calculate_c()

    def generate(self, iterations):
        values = defaultdict(int)

        for _ in range(iterations):
            y_value = self.y_gen()
            x_value = self.x_gen()

            while x_value > self.x_func(y_value) / (self.c * self.y_func(y_value)):
                y_value = self.y_gen()
                x_value = self.x_gen()
            values[y_value] += 1
        return values

    def calculate_c(self):
        return 0


class InverseTransform():
    ''' Given a distribution of probability p_i generates a random number with that
    probability distribution'''
    def __init__(self, p_i):
        if not isinstance(p_i, dict):
            raise ValueError("Weights must be a dict or a subclass of dict")
        # Sort the weights for improved efficency
        self.p_i = sorted(p_i.items(), key=lambda x: x[1], reverse=True)

    def generate(self, iterations):
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

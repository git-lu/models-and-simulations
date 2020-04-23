from math import gcd
from math import exp
from sympy import factorint
from sympy.ntheory.modular import solve_congruence
from sympy.ntheory.residue_ntheory import is_primitive_root
from sympy.ntheory.primetest import isprime

def isPrimitiveRoot(a,M):
#    primeFactors = list(factorint(M-1).keys())
#    res = all(((a**((M-1)/p)) % M) != (1 % M) for p in primeFactors)
    res = is_primitive_root(a,M)
    return res

class IntGenerator():
    def __init__(self,seed):
        self.sequence = []
        self.seed = seed
        self.generator = self.generateInt

    def generateInt(self,u):
        pass

    def generateNSecuence(self,n):
        '''
        Generates a n sequence numbers
        '''
        sequence=[self.seed]
        for i in range(n):
            sequence.append(self.generateInt(sequence[i]))
        self.sequence = sequence
        return self



class VonNeumann(IntGenerator):
    def __init__(self,seed):
        super().__init__(seed)
        

    def generateInt(self,u):
        '''
        Generates a random int from Von Neumman sequence
        '''
        if u >= 10000:
            raise ValueError("Seed must be an integer of 4 digits max!")
        else:
            u=((u**2)//100) %10000
        return u



class CongruentialGenerator(IntGenerator):
    def __init__(self,a,moduli,seed):
        super().__init__(seed)
        self.a = a
        self.moduli = moduli
        self.maxSequence = self.generatesMaxSequence()
    
    def generateInt(self,u):
        return (self.a*u) % self.moduli
    
    def generatesMaxSequence(self):
        ''' 
        The length K of a multiplicative congruence generator
        satisfies the following properties:
        - If K = M-1, then M is prime
        - K divides M -1
        - K = M - 1 if and only if a is a primitive root of M and M is prime
        '''
        res = isprime(self.moduli) and isPrimitiveRoot(self.a,self.moduli) 
        return res


 

class MixedCongruentialGenerator(CongruentialGenerator):
    def __init__(self,a,moduli,seed,c):
        self.c = c
        super().__init__(a,moduli,seed)
        
    def generateInt(self,u):
        return (self.a * u + self.c) % self.moduli

    def generatesMaxSequence(self):
        '''
        A mixed congruential generator generates a maximum
        period sequence if and only if:
        - mcd(c,M) = 1 (c and M coprimes)
        - a is congruent to 1 moduli p for every prime factor of M
        - if 4|M then a is congruent to 1 moduli 4
        '''
        firstCondition = self._GeneratesMaxPeriodFirstCondition(self.c,self.moduli)
        secondCondition = self._GeneratesMaxPeriodSecondCondition(self.a,self.moduli)
        thirdCondition = self._GeneratesMaxPeriodThirdCondition(self.a,self.moduli)
        res = firstCondition and secondCondition and thirdCondition
        return res

    def _GeneratesMaxPeriodFirstCondition(self,c,M):
        return gcd(c,M) == 1

    def _GeneratesMaxPeriodSecondCondition(self,a,M):
        # Calculate M prime factors
        MPrimeFactors = list(factorint(M).keys())
        # Calculate a congruent 1 mod p for each prime im M factorization
        congruences = all((a % prime) == (1 % prime) for prime in MPrimeFactors)
        return congruences
        
    def _GeneratesMaxPeriodThirdCondition(self,a,M):
        value = True
        # If 4|M then a is congruent to 1 moduli 4
        if M % 4 == 0:
            value = (a % 4) == 1
        else:
            value = True
        return value


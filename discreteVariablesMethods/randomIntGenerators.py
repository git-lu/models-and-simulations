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
    
    def generateInt(self,u):
        return (self.a*u) % self.moduli

 

class MixedCongruentialGenerator(CongruentialGenerator):
    def __init__(self,a,moduli,seed,c):
        super().__init__(a,moduli,seed)
        self.c = c
        
    def generateInt(self,u):
        return (self.a * u + self.c) % self.moduli


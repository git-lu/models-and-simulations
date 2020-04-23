from discreteVariablesMethods.randomIntGenerators import CongruentialGenerator
from discreteVariablesMethods.randomIntGenerators import MixedCongruentialGenerator

def test_congruentialGenerator():
    assert True


def test_mixedCongruentialGenerator():
    expectedResults = [
        [4, 24, 28, 16, 20, 8, 12, 0, 4, 24, 28],
        [50, 30, 26, 6, 2, 14, 10, 22, 18, 30, 26]
    ]
    a = 5
    c = 4
    M = 2**5
    n=10
    seeds = [4,50]
    results = []
    for seed in seeds:
        gen = MixedCongruentialGenerator(a=a,moduli=M,seed=seed,c=c)
        results.append(gen.generateNSecuence(n).sequence)
    assert expectedResults == results

def test_MaxSequenceCongruential():

    args = [(5,71),(7,71)]
    expectedResults = [False,True]    
    results = []

    for arg in args:
        results.append(CongruentialGenerator(a=arg[0],moduli=arg[1],seed=1).maxSequence)
    assert results == expectedResults

def test_MaxSequenceMixed():
    args = [(125,3,2**9),(123,3,2**9)]
    expectedResults = [True,False]
    results = []
    for arg in args:
        results.append(MixedCongruentialGenerator(a=arg[0],moduli=arg[2],c=arg[1],seed=1).maxSequence)
    assert results == expectedResults

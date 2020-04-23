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


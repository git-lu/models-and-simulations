from discreteVariablesMethods.randomIntGenerators import VonNeumann

def test_Sequence():
    expectedValues = [
        [3972, 7767, 3262, 6406, 368, 1354, 8333, 4388, 2545, 4770, 7529],
        [1004, 80, 64, 40, 16, 2, 0, 0, 0, 0, 0],
        [2100, 4100, 8100, 6100, 2100, 4100, 8100, 6100, 2100, 4100, 8100], 
        [1234, 5227, 3215, 3362, 3030, 1809, 2724, 4201, 6484, 422, 1780]
        ]
    n = 10
    seeds = [3972, 1004 ,2100, 1234]
    results = []
    for seed in seeds:
        vn = VonNeumann(seed).generateNSecuence(n)
        results.append(vn.sequence)
    assert expectedValues == results
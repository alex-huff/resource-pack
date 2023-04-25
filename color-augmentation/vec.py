import math

def roundAndTruncColor(vec):
    return \
    (
        truncateBand(round(vec[0])), 
        truncateBand(round(vec[1])), 
        truncateBand(round(vec[2]))
    )

def truncateBand(value):
    if (value > 255): return 255
    if (value < 0): return 0
    return value

def addVec(vecOne, vecTwo):
    return \
    (
        vecOne[0] + vecTwo[0],
        vecOne[1] + vecTwo[1],
        vecOne[2] + vecTwo[2]
    )

def subVec(vecOne, vecTwo):
    return \
    (
        vecOne[0] - vecTwo[0],
        vecOne[1] - vecTwo[1],
        vecOne[2] - vecTwo[2]
    )

def mulVec(vec, factor):
    return (vec[0] * factor, vec[1] * factor, vec[2] * factor)

def squaredDistance(vecOne, vecTwo):
    return \
        (vecOne[0] - vecTwo[0]) ** 2 + \
        (vecOne[1] - vecTwo[1]) ** 2 + \
        (vecOne[2] - vecTwo[2]) ** 2

def dotProduct(vecOne, vecTwo):
    return \
        (vecOne[0] * vecTwo[0]) + \
        (vecOne[1] * vecTwo[1]) + \
        (vecOne[2] * vecTwo[2])

def crosVec(vecOne, vecTwo):
    return \
    (
        vecOne[1] * vecTwo[2] - vecOne[2] * vecTwo[1],
        vecOne[2] * vecTwo[0] - vecOne[0] * vecTwo[2],
        vecOne[0] * vecTwo[1] - vecOne[1] * vecTwo[0]
    )

def normalizeVec(vec):
    return mulVec(vec, 1 / math.sqrt(dotProduct(vec, vec)))

def linearlyInterpolate(pointOne, pointTwo, factor):
    return addVec(pointOne, mulVec(subVec(pointTwo, pointOne), factor))

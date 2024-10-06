from math import exp, factorial





def UniformDistribution(x: float, a: float, b: float):
    if x < a:
        return 0
    elif x > b:
        return 1
    else:
        return (x - a) / (b - a)


def UniformDistributionDensity(x: float, a: float, b: float):
    if a <= x <= b:
        return 1 / (b - a)
    else:
        return 0


def PoissonDistribution(k: int, lambda_: float):
    
    if k < 0 :
        return 0
    return exp(-lambda_) * (lambda_ ** k) / factorial(k)


def PoissonDistributionDensity(k: int, lambda_: float):
    cdf = 0
    for i in range(k + 1):
        cdf += PoissonDistribution(i, lambda_)
    return cdf

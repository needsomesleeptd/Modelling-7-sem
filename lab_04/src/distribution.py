from math import erf, sqrt,exp,factorial

from numpy import log as ln
from numpy.random import normal
from random import random
import numpy as np 



class PoissonDistribution:
    def __init__(self, k: float, lambda_: float):
        if lambda_ <= 0:
            raise ValueError("lambda must be greater than 0")
        self.lambda_ = lambda_
        self.k = k

    def generate(self):
        if self.k < 0:
            return 0
        return np.random.poisson(self.lambda_)


class UniformDistribution:
    def __init__(self, a: float, b: float):
        if a >= b:
            raise ValueError("a must be less than b")
        self.a = a
        self.b = b

    def generate(self):
        x = np.random.uniform(self.a, self.b)
        return x
    









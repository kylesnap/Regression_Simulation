#!usr/bin/env python
# simulation.py
# Kyle Dewsnap
# July 8th
from typing import Tuple, Any
from nptyping import NDArray
from scipy.stats import norm, uniform
import numpy as np

REPS = 10

class Cell:
    def __init__(self, params: Tuple):
        self._params = params
        self._n = params[0]
        self._b1 = params[1]
        self._cdist = norm(loc = params[2], scale = params[3])
        self._cp = params[4]

    def __str__(self) -> str:
        " Prints the n, b1, cdist, and cp of the cell. "
        return ",".join(map(str, self._params))

    def run(self) -> None:
        """ Makes design matrix, then does REPS number of reps of making
        random errors, making true data, then fitting and printing model. """
        d_mat = self.mk_dmat()
        print(d_mat)

    def mk_dmat(self) -> NDArray[(Any, 2), np.float64]:
        """ Generates a matrix with all ones in first col, and a uniformly
        distributed X1 variable. """
        x1_gen = uniform(loc = 0, scale = 1)
        mat = np.array([[0, x1_gen.rvs()] for i in range(self._n)])
        return(mat)


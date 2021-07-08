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
        self._odist = norm(loc = params[2], scale = params[3])
        self._op = params[4]

    def __str__(self) -> str:
        """ Prints the n, b1, odist, and op of the oell. """
        return ",".join(map(str, self._params))

    def run(self) -> None:
        """ Makes design matrix, then does REPS number of reps of making
        random errors, making true data, then fitting and printing model. """
        d_mat = self.mk_dmat()
        errs = self.mk_errors()
        print(errs)

    def mk_dmat(self) -> NDArray[(Any, 2), np.float64]:
        """ Generates a matrix with all ones in first col, and a uniformly
        distributed X1 variable. """
        x1_gen = uniform(loc = 0, scale = 1)
        return np.array([[0, x1_gen.rvs()] for i in range(self._n)])

    def mk_errors(self) -> NDArray[(1), np.float64]:
        """ Generates an array with error terms, with N*OP outliers.
        Error terms are from N(0,1), with outlier terms from odist. """
        rdist = norm(loc = 0, scale = 1)
        return np.array([self._odist.rvs() if
            np.random.random() <= self._op else rdist.rvs() for
            i in range(self._n)])

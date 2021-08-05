#!usr/bin/env python
# simulation.py
# Kyle Dewsnap
# July 8th
from typing import Tuple, Any, TextIO
from nptyping import NDArray
from scipy.stats import norm, uniform
import numpy as np
import ols_lm

REPS = 10
B0 = 0

class Cell:
    def __init__(self, params: Tuple, handle: TextIO):
        self._params = params
        self._n = params[0]
        self._b1 = 1
        self._fdist = norm(loc = params[1], scale = 1) # Focal dist.
        self._op = params[2]
        self._handle = handle

    def __str__(self) -> str:
        """ Prints the n, b1, odist, and op of the oell. """
        return ",".join(map(str, self._params))

    def run(self) -> None:
        """ Makes design matrix, then does REPS number of reps of making
        random errors, making true data, then fitting and printing model. """
        trial = str(self)
        d_mat = self.mk_dmat() # Deterministic component
        for i in range(REPS):
            y = self.mk_y(d_mat, self.mk_errors()) # Adds stochastic component
            mod = ols_lm.OLS_Lm(d_mat, y)
            mod.fit_lm()
            self._handle.write("%d,%s,%s\n" % (i + 1, trial, str(mod)))

    def mk_dmat(self) -> NDArray[(Any, 2), np.float64]:
        """ Generates a matrix with all ones in first col, and a uniformly
        distributed X1 variable in the second. """
        x1_gen = uniform(loc = 0, scale = 1)  # U[0,1]
        return np.array([[1, x1_gen.rvs()] for i in range(self._n)])

    def mk_errors(self) -> NDArray[(1), np.float64]:
        """ Generates an array with error terms with N*OP outliers.
        Error terms are from N(0,1), with outlier terms from odist. """
        rdist = norm(loc = 0, scale = 1) #N(0,1) (Reference distribution)
        return np.array([self._fdist.rvs() if
            np.random.random() <= self._op else rdist.rvs() for
            i in range(self._n)])

    def mk_y(self, d_mat: NDArray, errs: NDArray) -> NDArray[(1), np.float64]:
        """ Generates a vector with observed response terms, generated from
        a true data generating mechanism """
        return np.matmul(d_mat, np.array([B0, self._b1])) + errs

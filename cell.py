#!usr/bin/env python
# simulation.py
# Kyle Dewsnap
# July 8th
from typing import Tuple, Any, TextIO
from nptyping import NDArray
from scipy.stats import norm, uniform
import numpy as np
import ols_lm

REPS =  5000
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
            errs = self.mk_errors()
            y = self.mk_y(d_mat, errs) # Adds stochastic component
            mod = ols_lm.OLS_Lm(d_mat, y)
            mod.fit_lm()
            self._handle.write("%d,%s,%f,%f,%s\n" %
                    (i + 1, trial, np.mean(errs), np.std(errs), str(mod)))

    def mk_dmat(self) -> NDArray[(Any, 2), np.float64]:
        """ Generates a matrix with all ones in first col, and a uniformly
        distributed X1 variable in the second. """
        x1_gen = uniform(loc = 0, scale = 1)  # U[0,1]
        return np.array([[1, x1_gen.rvs()] for i in range(self._n)])

    def mk_errors(self) -> NDArray[(1), np.float64]:
        """ Generates an array with error terms with N*OP outliers.
        Error terms are from N(0,1), with outlier terms from odist. """
        rdist = norm(loc = 0, scale = 1) #N(0,1) (Reference distribution)
        out_errs = np.array([self._fdist.rvs() for i in
            range(np.floor(self._n * self._op).astype('int'))])
        norm_errs = np.array([rdist.rvs() for i in
            range(self._n - np.floor(self._n * self._op).astype('int'))])
        errs = np.concatenate((out_errs, norm_errs), axis=None)
        np.random.shuffle(errs)
        return errs - np.mean(errs)

    def mk_y(self, d_mat: NDArray, errs: NDArray) -> NDArray[(1), np.float64]:
        """ Generates a vector with observed response terms, generated from
        a true data generating mechanism """
        return np.matmul(d_mat, np.array([B0, self._b1])) + errs

if __name__=="__main__":
    """ Test error generation. """
    p1 = Cell((100000, 2.68, 0.01), None).mk_errors()
    p25 = Cell((100000, 2.68, 0.025), None).mk_errors()
    p5 = Cell((100000, 2.68, 0.05), None).mk_errors()

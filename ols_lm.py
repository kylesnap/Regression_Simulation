#!usr/bin/env python
# ols_lm.py
# Kyle Dewsnap
# July 9th

from nptyping import NDArray
import numpy as np
import unittest

class OLS_Lm:
    def __init__(self, dmat: NDArray, y: NDArray, fit = True):
        self._pred = dmat
        self._resp = y
        self._beta = None
        self._beta_se = None
        self._rsq = None

    def __str__(self) -> str:
        """ Prints b0, b1, bse1, bse2 """
        return(str("%f,%f,%f,%f,%f" % (
            self._beta[0],
            self._beta[1],
            self._beta_se[0],
            self._beta_se[1],
            self._rsq
            )))

    def fit_lm(self) -> NDArray[(1), np.float64]:
        """ Performs matrix algebra to fit data to simple OLS model (number of
        betas == k + 1 (beta_0, beta_1, ..., beta_k) """
        ols_est = lambda X, Y: np.matmul( # betas = (X'X)^-1 * X'Y
                np.linalg.inv(np.matmul(np.transpose(X), X)),
                np.matmul(np.transpose(X), Y))
        res = lambda X, Y, BETA: Y - np.matmul(X, BETA) # e = Y - X*betas
        sigma = lambda X, Y, BETA: np.matmul( # sigma^2 = e'e / n - k
                np.transpose(res(X, Y, BETA)),
                res(X, Y, BETA)
                ) / (X.shape[0] - X.shape[1])
        ols_cov = lambda X, Y, BETA: sigma(X, Y, BETA) * \
                np.linalg.inv(np.matmul(np.transpose(X), X)) # COV=sigma(X'X)^-1
        self._beta = ols_est(self._pred, self._resp)
        self._beta_se = np.sqrt( # SE_BETA = sqrt of the diagonal of the V-COV
                np.diagonal(ols_cov(self._pred, self._resp, self._beta))
                )
        self._rsq = (# R^2 == cor(Y, Y_hat)**2
                np.corrcoef(
                    self._resp, res(self._pred, self._resp, self._beta)
                    )**2
                )[0][1]

class TestOLS(unittest.TestCase):

    def test_nullmod(self):
        test_pred = np.array([[i, 0] for i in range(100)])
        test_resp = np.array([[i] for i in range(100)])
        test_mod = OLS_Lm(test_pred, test_resp)
        test_mod.fit_lm()
        self.assertEqual(test_mod._beta[0], 1)

    def test_mod2(self):
        test_pred = np.array([[1,i] for i in range(100)])
        test_resp = np.array([[i] for i in range(100)])
        test_mod = OLS_Lm(test_pred, test_resp)
        test_mod.fit_lm()
        self.assertAlmostEqual(test_mod._beta[0], 0)
        self.assertAlmostEqual(test_mod._beta[1], 1)

if __name__ == "__main__":
    unittest.main()


#!usr/bin/env python
# simulation.py
# Kyle Dewsnap
# July 5th
from typing import Dict
import itertools
import cell

class Simulation:
    def __init__(self, parameters: Dict):
        self._params = parameters
        self._p_lst = [[2],[0,1],[2],[0],[0]]
        # When not testing, list(parameters.values())

    def run(self) -> None:
        """ Confirms that parameters are acceptable, then creates and runs
        all cells."""
        print(self._params)
        all_cells = [x for x in itertools.product(*self._p_lst)]
        for i in all_cells:
            exp = cell.Cell(i)
            print("Running Cell:", exp)
            exp.run()

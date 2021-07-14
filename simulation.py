#!usr/bin/env python
# simulation.py
# Kyle Dewsnap
# July 5th
from typing import Dict, TextIO
import itertools
import cell
import warnings

class Simulation:
    def __init__(self, parameters: Dict, log: TextIO):
        self._params = parameters
        self._p_lst = list(parameters.values())
        self._log = log

    def run(self) -> None:
        """ Confirms that parameters are acceptable, then creates and runs
        all cells."""
        print(self._params)
        all_cells = [x for x in itertools.product(*self._p_lst)]
        if self._log:
            with self._log as f:
                f.write("R,N,B1,OM,OV,OP,BT0,BT1,BTSE0,BTSE1\n")
                for i in all_cells:
                    exp = cell.Cell(i, f)
                    print("Running cell: %s" % str(exp))
                    exp.run()
        else:
            warnings.warn("Logging has been disabled. Printing to STDOUT.")
            print("R,N,B1,OM,OV,OP,BT0,BT1,BTSE0,BTSE1")
            for i in all_cells:
                exp = cell.Cell(i)
                print("Running cell: %s" % str(exp))
                exp.run()

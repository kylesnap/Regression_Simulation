#!usr/bin/env python
# simulation.py
# Kyle Dewsnap
# July 5th
from typing import Dict
import itertools
import cell
import sys

class Simulation:
    def __init__(self, parameters: Dict, log: str):
        self._params = parameters
        self._p_lst = list(parameters.values())
        self._log = log

    def run(self) -> None:
        """ Confirms that parameters are acceptable, then creates and runs
        all cells. """
        print(self._params)
        confirm = input("Run? (Use Cntl + C to Cancel) [Y/y]: ").lower()
        if confirm != "y":
            print("Cancelling simulation.")
            exit(1)
        handle = open(self._log, "w") if self._log else sys.stdout
        all_cells = [x for x in itertools.product(*self._p_lst)]
        handle.write("R,N,B1,OM,OV,OP,BT0,BT1,BTSE0,BTSE1\n")
        for i in all_cells:
            exp = cell.Cell(i, handle)
            print("Running cell: %s" % str(exp), file=sys.stdout)
            exp.run()
        if handle is not sys.stdout: handle.close()

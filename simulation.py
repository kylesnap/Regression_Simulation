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
        self._all_cells = [x for x in itertools.product(
            *list(parameters.values()))]
        # Log can take the value of a string or of NONE if no logging done.
        self._log = log

    def run(self) -> None:
        """ runs all cells. """
        handle = open(self._log, "w") if self._log else sys.stdout
        handle.write("I,N,OM,OP,EM,ESD,BT0,BT1,BTSE0,BTSE1,R_SQ\n")
        for i in self._all_cells:
            exp = cell.Cell(i, handle)
            print("Running cell: %s" % str(exp), file=sys.stdout)
            exp.run()
        if handle is not sys.stdout: handle.close()

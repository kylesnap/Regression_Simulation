#!/usr/bin/env python3
# main.py
# Kyle Dewsnap
# 28JUN21

import argparse
from datetime import datetime
import random
import logging
from typing import Dict
import simulation

def main() -> None:
    """ Parses command line arguments, gets simulation parameters, then
    constructs and builds Simulation"""

    start_log()
    params = {"Test": 1} # get_params()
    sim = simulation.Simulation(params)
    sim.run()

def start_log() -> None:
    """ Starts log file. """
    now = datetime.now()

    parser = argparse.ArgumentParser(description="Runs simulation.")
    parser.add_argument("--noseed", "-n", action="store_true",
                        help="do not seed the next simulation")
    parser.add_argument("--logname", type = str,
                        default=str("sim_%s_%s" %
                                    (now.strftime("%x"), now.strftime("%X"))),
                        help="name of the log files written by simulation")
    parser.add_argument("--log", "-l", action="store_true",
                        help="prints log file")
    args = parser.parse_args()

    if args.noseed:
        random.seed()
    else:
        logging.warning("This run is seeded.")
        random.seed(69) # Nice

    if args.log:
        logfile = "./log/" + args.logname + ".log"
        logging.basicConfig(filename=logfile, level=logging.INFO)

def get_params() -> Dict:
    """ Returns a dictionary of simulation parameters """
    in_n = input("Input space-separated list of N: ")
    in_b1 = input("Input space-separated list of true B1: ")
    in_om = input("Input space-separated list of means of the outlier "
            "distribution: ")
    in_ov = input("Input space-separated list of vars. of the outlier "
        "distribution: ")
    in_op = input("Input space-separated list of prop. of outliers to "
            "add: ")

    try:
        lst_n = [int(x) for x in in_n.split(" ")]
        lst_b1 = [float(x) for x in in_b1.split(" ")]
        lst_om = [float(x) for x in in_om.split(" ")]
        lst_ov = [float(x) for x in in_ov.split(" ")]
        lst_op = [float(x) for x in in_op.split(" ") if 0 <= float(x) <= 1]
    except (TypeError, ValueError):
        print("The arguments failed to parse. Try again.")
        return get_params()

    return{"n": lst_n, "b1": lst_b1, "om" : lst_om,
            "ov" : lst_ov, "op" : lst_op}

if __name__ == "__main__":
    main()

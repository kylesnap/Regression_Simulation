#!/usr/bin/env python3
# main.py
# Kyle Dewsnap
# 28JUN21

import argparse
from datetime import datetime
import random
import logging
from typing import Dict

def main() -> None:
    """ Parses command line arguments, gets simulation parameters, then
    constructs and builds Simulation"""
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
    params = get_params()
    print(params)

def get_params() -> Dict:
    """ Returns a dictionary of simulation parameters """
    in_n = input("Input space-separated list of N to try: ")
    in_b1 = input("Input space-separated list of true B1 to try: ")

    try:
        lst_n = [int(x) for x in in_n.split(" ")]
        lst_b1 = [float(x) for x in in_b1.split(" ")]
    except (TypeError, ValueError):
        print("The arguments failed to parse. Try again.")
        return get_params()

    return{'n': lst_n, 'b1': lst_b1}

if __name__ == "__main__":
    main()

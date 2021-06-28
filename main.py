#!/usr/bin/env python3
# main.py
# Kyle Dewsnap
# 28JUN21

import argparse
from datetime import datetime
import random
import logging

def main() -> None:
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

if __name__ == "__main__":
    main()

# main.py
# Kyle Dewsnap
# 24JUL21

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import datetime
import random
import simulation
import warnings

def parse_params():
    """ Returns a dictionary of simulation parameters """
    try:
        lst_n = [int(x) for x in samples.get().split(" ") if int(x) > 1]
        lst_fm = [float(x) for x in fmeans.get().split(" ")]
        lst_fp = [float(x) for x in fprops.get().split(" ") if
                0 <= float(x) < 0.5]
    except (TypeError, ValueError):
        messagebox.showerror("Error", "Error parsing lists of parameters.")
        return

    if not lst_n or not lst_fm or not lst_fp:
        messagebox.showerror("Error", "Missing values for all parameters.")
        return

    params = {"n": lst_n, "fm": lst_fm, "fp": lst_fp, "seed": seed.get(), "log":
        log.get()}
    start_sim(params)

def start_sim(params):
    """ Runs the simulation with dictionary of parameters. """
    if params.pop("seed") is False:
        random.seed()
    else:
        warnings.warn("This run is seeded.")
        random.seed(66) # Nice

    if params.pop("log") is True:
        logname = datetime.now.strftime("./log/sim_%d%b%y_%-H%M.csv")
    else:
        logname = None

    print(params)
    check = None
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        check = messagebox.askokcancel("Confirm?",
                "Check terminal for correct params")
    if check:
        sim = simulation.Simulation(params, logname)
        sim.run()
        root.destroy()
        exit(0)
    else:
        return

root = Tk()
root.title("K.D.'s OLS Simulation.")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

head = ttk.Label(mainframe, text="Space Seperated Lists of Parameters").grid(
        column=0, row=0)

samples = StringVar()
ttk.Label(mainframe, text="Sample sizes [2, Inf]", font="TkMenuFont").grid(
        column=0, row=1, sticky=(W, E))
samples_entry = ttk.Entry(mainframe, width=10, textvariable=samples)
samples_entry.grid(column=1, row=1, sticky=(W, E))

fmeans = StringVar()
ttk.Label(mainframe, text="Focal distribution means", font="TkMenuFont").grid(
        column=0, row=2, sticky=(W, E))
fmeans_entry = ttk.Entry(mainframe, width=10, textvariable=fmeans)
fmeans_entry.grid(column=1, row=2, sticky=(W, E))

fprops = StringVar()
ttk.Label(mainframe, text="Proportion of deviants [0, 0.5)",
        font="TkMenuFont").grid(column=0, row=3, sticky=(W, E))
fprops_entry = ttk.Entry(mainframe, width=10, textvariable=fprops)
fprops_entry.grid(column=1, row=3, sticky=(W, E))

seed = BooleanVar(value=True)
ttk.Checkbutton(mainframe, text="Seed random", variable=seed).grid(
        column=0, row=4, sticky=(W, E))
log = BooleanVar(value=False)
ttk.Checkbutton(mainframe, text="Save log file", variable=log).grid(
        column=1, row=4, sticky=(W, E))

note = ttk.Label(mainframe,
        text="Terminal will display warnings and progess.").grid(
        column=0, row=0)

ttk.Button(mainframe, text="Run Simulation!", command=parse_params).grid(
        column=0, row=5, sticky=(W, E))

root.mainloop()

from math import ceil, floor
from matplotlib.pyplot import subplots, show as show_plots
from numpy import zeros


def plot(x, y):
    fig, ax = subplots()
    ax.plot(x, y)
    show_plots(block=False)


def stem(x, y):
    fig, ax = subplots()
    ax.stem(x, y)
    show_plots(block=False)


def sample(x, fs, s, e):
    n = floor((e - s) * fs)

    y = zeros(n)
    for i in range(0, n):
        y[i] = x[i * r] 
    
    return y
    

# vim: ai: et: ts=4: sts=4

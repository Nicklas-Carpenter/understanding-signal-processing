from math import ceil, floor
from matplotlib.pyplot import subplots, show as show_plot
from numpy import linspace
from sympy import (
    Eq, dsolve, Function, symbols, srepr, sympify, Heaviside, Piecewise,
    lambdify, pprint, fourier_transform as fou_trans , integrate, exp, I
)


t, w = symbols("t, w", real=True)
u = Heaviside 


def square_wave(A=1, T=1, d=0.5, c=0, n=1):
    if n <= 0 or A < 0 or T <=0 or d <=0:
        raise ValueError()

    sw = 0
    for k in range(-floor(n/2), ceil(n/2)):
        a = ((k + c) * T) + (d * (T / 2))
        sw = sw + A * (u(t + a) - u(t - a))

    if n % 2 == 0:
        sw = -sw
    return sw


def lowpass_filter(signal, R=1, C=1, start=-10000):
    y = symbols("y", cls=Function, real=True)
    diff_eq = Eq(y(t) + R * C * y(t).diff(t), signal) 
    sol = dsolve(diff_eq, y(t), ics={y(start): 0})
    return sol.rhs


def highpass_filter(signal, R=1, C=1, start=-10000):
    y = symbols("y", cls=Function, real=True)
    diff_eq = Eq(y(t)/R + C*y(t).diff(t), signal.diff(t)) 
    sol = dsolve(diff_eq, y(t), ics={y(start): 0})
    return sol.rhs


def sig_plot(signal, start, end, np=None):
    if np is None:
        np = (end - start) * 10000

    fn = lambdify(t, signal)
    tt = linspace(start, end, np)
    y = fn(tt)

    fig, ax = subplots()
    ax.plot(tt, y)
    show_plot(block=False) 


def fourier_transform(signal):
    return fou_trans(signal, t, w)


def heuristic_fourier_transform(signal, lb=-1000, up=1000):
    return integrate(signal * exp(-I * w * t), (t, lb, up))


def fourier_plot(spectrum, start, end, np=None):
    if np is None:
        np = (end - start) * 10000

    fn = lambdify(w, spectrum)
    ww = linspace(start, end, np)
    y = fn(ww)

    fig, ax = subplots()
    ax.plot(ww, y)
    show_plot(block=False) 


# vim: ai: et: sts=4: ts=4

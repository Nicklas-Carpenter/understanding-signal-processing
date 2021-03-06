from math import ceil, floor
from matplotlib.pyplot import subplots, show as show_plot
from numpy import linspace, abs
from sympy import (
    Eq, dsolve, Function, symbols, srepr, sympify, Heaviside, Piecewise,
    lambdify, pprint, fourier_transform as fou_trans, integrate, exp, I
)


t, w, T, k, d, R, C = symbols("t w T k d R C", real=True)
u = Heaviside 

a = T*(k + d/2)
rect = u(t + a) - u(t - a)
rect_base = rect.subs([(T, 1), (k, 0), (d, 0.5)])
rect_ft_base = fou_trans(rect_base, t, w)

y = symbols("y", cls=Function, real=True)
lowpass_rect_system = Eq(y(t) + R*C*y(t).diff(t), rect)
lowpass_rect_sol = dsolve(lowpass_rect_system, y(t))
C1 = symbols("C1")
rect_lresp_base = lowpass_rect_sol.rhs.subs(C1, 0)

H_lowpass_template = 1 / (R*I*w*C + 1)


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
    y = abs(fn(ww))

    fig, ax = subplots()
    ax.plot(ww, y)
    show_plot(block=False) 


def fourier_transform_rect_sequence(n, TT, dd):
    ft = 0

    for kk in range(-floor(n/2), ceil(n/2)):
        aa = a.subs([(k, kk), (d, dd), (T, TT)]) 
        ft = ft + rect_ft_base * exp(-I * w * aa)

    return ft


def rect_lowpass_filter_response_sequence(n, TT, dd, RR, CC):
    lresp_base = rect_lresp_base.subs([(T, TT), (d, dd), (R, RR), (C, CC)])

    lresp = 0
    for kk in range(-floor(n/2), ceil(n/2)):
        lresp = lresp + lresp_base.subs(k, kk)

    return lresp


def square_wave_system(TT=1, dd=0.5, RR=1, CC=1, n=1):
    s = square_wave(A=1, T=TT, d=dd, n=n)
    s_ft = fourier_transform_rect_sequence(n, TT, dd) 

    H_lowpass = H_lowpass_template.subs([(R, RR), (C, CC)])
    f_lresp = s_ft * H_lowpass 
    lresp = rect_lowpass_filter_response_sequence(n, TT, dd, RR, CC)

    s_lambda = lambdify(t, s)
    s_ft_lambda = lambdify(w, s_ft)
    f_lresp_lambda = lambdify(w, f_lresp)
    lresp_lambda = lambdify(t, lresp)

    tt = linspace(-12, 12, 240000)
    ww = linspace(-12, 12, 240000)

    s_output = s_lambda(tt)
    s_ft_output = s_ft_lambda(ww)
    f_lresp_output = f_lresp_lambda(ww)
    lresp_output = lresp_lambda(tt)

    fig0, (ax0, ax1) = subplots(1, 2)
    fig1, (ax2, ax3) = subplots(1, 2)
    ax0.plot(tt, s_output)
    ax1.plot(tt, lresp_output)
    ax2.plot(ww, abs(s_ft_output))
    ax3.plot(ww, abs(f_lresp_output))



# vim: ai: et: sts=4: ts=4

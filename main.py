import math

from sympy import Interval
import numpy as np
from plot_intervals import  plot_line_intervals, plot_rectangles
import scipy.optimize

def getMulMin(a: Interval, b: Interval):
    return min(min(a.inf * b.inf, a.inf * b.sup), min(a.sup * b.inf, a.sup * b.sup))

def getMulMax(a: Interval, b: Interval):
    return max(max(a.inf * b.inf, a.inf * b.sup), max(a.sup * b.inf, a.sup * b.sup))

def absMin(a, b):
    if math.fabs(a) < math.fabs(b):
        return a
    return b

def function1(x):
    return math.sin(x)

def function2(x):
    return math.exp(x)

def check1(x, y, err, params):
    for i in range(len(err)):
        interval = Interval(-err[i], err[i])
        func = Interval(function1(x[i]), function1(x[i]))
        a = (y[i] - getMulMax(func, params))
        b = (y[i] - getMulMin(func, params))
        new_params = Interval(a, b)
        if interval.intersection(new_params).is_empty:
            return False
    return True

def check2(x, y, err, params1, params2):
    for i in range(len(err)):
        interval = Interval(-err[i], err[i])
        a = y[i] - params2.sup * (function2(x[i] + params1.sup))
        b = y[i] - params2.inf * (function2(x[i] + params1.inf))
        new_params = Interval(a, b)
        if interval.intersection(new_params).is_empty:
            return False
    return True

def methodMoore1(eps, startParam: Interval, x, y, err):
    result = [startParam]
    while len(result) > 0 and result[0].sup - result[0].inf > eps:
        section1 = Interval((result[0].inf + result[0].sup) / 2, result[0].sup)
        section2 = Interval(result[0].inf, (result[0].inf + result[0].sup) / 2)
        result.pop(0)
        if check1(x, y, err, section1):
            result.append(section1)
        if check1(x, y, err, section2):
            result.append(section2)
    return result

def methodMoore2(eps, startParam1: Interval, startParam2: Interval, x, y, err) -> []:
    if max(startParam1.sup - startParam1.inf, startParam2.sup - startParam2.inf) > eps:
        if startParam2.sup - startParam2.inf > startParam1.sup - startParam1.inf:
          section2 = Interval(startParam2.inf, (startParam2.sup + startParam2.inf) / 2)
          list1 = []
          if check2(x, y, err, startParam1, section2):
            list1 = methodMoore2(eps, startParam1, section2, x, y, err)
          section2 = Interval((startParam2.sup + startParam2.inf) / 2, startParam2.sup)
          list2 = []
          if check2(x, y, err, startParam1, section2):
            list2 = methodMoore2(eps, startParam1, section2, x, y, err)
          return list1 + list2
        else:
            section1 = Interval(startParam1.inf, (startParam1.sup + startParam1.inf) / 2)
            list1 = []
            if check2(x, y, err, section1, startParam2):
                list1 = methodMoore2(eps, section1, startParam2, x, y, err)
            section1 = Interval((startParam1.sup + startParam1.inf) / 2, startParam1.sup)
            list2 = []
            if check2(x, y, err, section1, startParam2):
                list2 = methodMoore2(eps, section1, startParam2, x, y, err)
            return list1 + list2
    else:
        if check2(x, y, err, startParam1, startParam2):
            return [[startParam1, startParam2]]
        else:
            return []

def simplex_method(x, y, err, func):
    c = []
    A = []
    b = []
    bounds = []
    c.append(0)
    bounds.append((None, None))
    for i in range(len(x)):
        c.append(1)
        bounds.append((0, None))
        elem1 = [0 for i in range(len(y) + 1)]
        elem2 = [0 for i in range(len(y) + 1)]
        elem1[0] = -func(x[i])
        elem1[i + 1] = -err[i]
        A.append(elem1)
        b.append(err[i] - y[i])
        elem2[0] = func(x[i])
        elem2[i + 1] = -err[i]
        A.append(elem2)
        b.append(y[i] + err[i])
    return scipy.optimize.linprog(c, A_ub=A, b_ub=b, bounds=tuple(bounds))

def new_data(simplex_x, x, y, err):
    new_x = []
    new_y = []
    new_err = []
    for i in range(len(x)):
        if simplex_x[i + 1] < 10 ** (-1):
            new_x.append(x[i])
            new_y.append(y[i])
            new_err.append(err[i])
    return new_x, new_y, new_err

N = 10
eps = 0.5
x = [x for x in range(N)]
err = [eps] * N
y = [10 * function1(x) + eps * np.random.normal(0, 1, size=1)[0] for x in range(N)]
startParam = Interval(8, 13)

res = simplex_method(x, y, err, function1)
print(res)
x1, y1, err1 = new_data(res.x, x, y, err)
plot_line_intervals(methodMoore1(0.005, startParam, x1, y1, err1))

y = [9 * function2(x + 5) + np.random.normal(0, 1, size=1)[0] for x in range(N)]
startParam1 = Interval(3, 6)
startParam2 = Interval(5, 15)

res = simplex_method(x, y, err, function2)
print(res)
x1, y1, err1 = new_data(res.x, x, y, err)
plot_rectangles(methodMoore2(0.005, startParam1, startParam2, x1, y1, err1))

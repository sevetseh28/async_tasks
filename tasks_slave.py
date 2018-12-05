from __future__ import absolute_import, unicode_literals

import time
from collections import defaultdict

import celery
from celery import Celery
from sympy import integrate, Symbol


app = Celery('tasks_project', broker='amqp://broker', backend='amqp://broker')


@celery.task(name='Integrate')
def integration(coefficients: list):
    """
    :param coefficients: list of the coefficients from lower to higher exponent order
    :return:
    """
    time.sleep(10)
    x = Symbol('x')
    polynomial = 0
    for idx, coeff in enumerate(coefficients):
        polynomial += coeff * x ** idx
    r = integrate(polynomial)
    print(str(r))
    return str(r)


@celery.task(name='Prime factoring')
def prime_factoring(nr):
    time.sleep(10)
    ret = defaultdict(int)
    i = 2
    while i <= nr:
        if (nr % i) == 0:
            ret[i] += 1
            nr = nr / i
        else:
            i = i + 1
    return ret

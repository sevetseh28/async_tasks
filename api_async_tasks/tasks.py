from __future__ import absolute_import, unicode_literals
import os
import time
from collections import defaultdict

import celery
from sympy import integrate, Symbol

from celery import Celery

# set the default Django settings module for the 'celery' program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tasks_project.settings')

app = Celery('tasks_project', broker='amqp://broker',
             # backend='db+postgresql+psycopg2://postgres:holahola@localhost/tasks_project',
             backend='amqp://broker')


# app.conf.database_engine_options = {'encoding': 'utf-8'}


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
# app.autodiscover_tasks()


@celery.task(name='Integrate')
def integration(coefficients: list):
    """
    :param coefficients: list of the coefficients from lower to higher exponent order
    :return:
    """
    x = Symbol('x')
    polynomial = 0
    for idx, coeff in enumerate(coefficients):
        polynomial += coeff * x ** idx
    r = integrate(polynomial)
    print(str(r))
    return str(r)


@celery.task(name='Prime factoring')
def prime_factoring(nr):
    ret = defaultdict(int)
    i = 2
    # factors = []
    while i <= nr:
        if (nr % i) == 0:
            ret[i] += 1
            # factors.append(i)
            nr = nr / i
        else:
            i = i + 1
    return ret

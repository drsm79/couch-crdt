import inspect
import requests
from posixpath import join

server = 'http://localhost:5984/'


def print_counter(c, log=False):
    print 'ln: %s counter: %s' % (
        inspect.getouterframes(inspect.currentframe())[1][2],
        c
    )
    if log:
        print_log()


def print_log():
    print requests.get(join(server, '_log')).text.split('\n')[-2:-1]

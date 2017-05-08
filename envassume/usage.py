# -*- coding: utf-8 -*-
"""
envassume exceptions
"""

from __future__ import print_function
import sys


def print_help(short = False):
    print('usage: envassume [-h] [-i EXTERNAL_ID] [ARN] command [argument [argument ...]]', file = sys.stderr)
    if not short:
        print('''
positional arguments:

    command                 command to run
    argument                command arguments

optional arguments:
    -h, --help              show this help message and exit
    -i, --id EXTERNAL_ID    external id
    ARN                     ARN to assume (if not set by environment variable)
''', file = sys.stderr)


def print_error(message):
    print_help(short = True)
    print('error: {}'.format(message), file = sys.stderr)

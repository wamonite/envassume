# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import
import pytest
import mock
from envassume.usage import print_help, print_error
import sys


@pytest.mark.parametrize('short', (True, False))
def test_help(short, monkeypatch):
    print_func = mock.Mock()
    if sys.version_info[0] >= 3:
        monkeypatch.setattr('builtins.print', print_func)
    else:
        monkeypatch.setattr('__builtin__.print', print_func)
    print_help(short)
    calls = print_func.call_args_list
    assert calls[0][0][0].startswith('usage:')


@pytest.mark.parametrize('message', ('message', 'foo'))
def test_error(message, monkeypatch):
    print_func = mock.Mock()
    if sys.version_info[0] >= 3:
        monkeypatch.setattr('builtins.print', print_func)
    else:
        monkeypatch.setattr('__builtin__.print', print_func)
    print_error(message)
    calls = print_func.call_args_list
    assert calls[0][0][0].startswith('usage:')
    assert calls[1][0][0].startswith('error:')
    assert message in calls[1][0][0]

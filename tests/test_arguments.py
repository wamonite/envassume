# -*- coding: utf-8 -*-

from __future__ import print_function
from envassume.arguments import parse_arguments
from envassume.exceptions import (
    EnvAssumeMissingArnException,
    EnvAssumeHelpException,
    EnvAssumeArgumentException,
    EnvAssumeMissingCommandException,
)
import pytest
from attr import attrs, attrib, validators


@attrs
class ParseArgsResult(object):
    arn = attrib()
    command = attrib(default = [], validator = validators.instance_of(list))
    external_id = attrib(default = None)
    cache = attrib(default = None)


@pytest.mark.parametrize('arg_list, parse_args_result', [
    (['arn', 'cmd'], ParseArgsResult('arn', ['cmd'])),
    (['arn', 'cmd', 'arg'], ParseArgsResult('arn', ['cmd', 'arg'])),
    (['arn', '--', 'cmd'], ParseArgsResult('arn', ['cmd'])),
    (['arn', '--', 'cmd', 'arg'], ParseArgsResult('arn', ['cmd', 'arg'])),
    (['--id', 'id', 'arn', 'cmd'], ParseArgsResult('arn', ['cmd'], 'id')),
    (['--id=id', 'arn', 'cmd'], ParseArgsResult('arn', ['cmd'], 'id')),
    (['-i', 'id', 'arn', 'cmd'], ParseArgsResult('arn', ['cmd'], 'id')),
])
def test_parse_args(arg_list, parse_args_result):
    result = parse_arguments(['arg0'] + arg_list)
    assert result.get('arn') == parse_args_result.arn
    assert result.get('external_id') == parse_args_result.external_id
    assert result.get('cache') == parse_args_result.cache
    assert result.get('command') == parse_args_result.command


@pytest.mark.parametrize('arg_list, exception', [
    ([], EnvAssumeMissingArnException),
    (['--'], EnvAssumeMissingArnException),
    (['-i', 'id'], EnvAssumeMissingArnException),
    (['-i', 'id', '--'], EnvAssumeMissingArnException),
    (['-h'], EnvAssumeHelpException),
    (['--help'], EnvAssumeHelpException),
    (['-z'], EnvAssumeArgumentException),  # unknown
    (['--ida='], EnvAssumeArgumentException),  # invalid
    (['arn'], EnvAssumeMissingCommandException),
    (['arn', '--'], EnvAssumeMissingCommandException),
])
def test_parse_args_errors(arg_list, exception):
    with pytest.raises(exception):
        parse_arguments(['arg0'] + arg_list)

# -*- coding: utf-8 -*-

from __future__ import print_function
from envassume.main import apply_session_name_constraints, EnvAssumeException

import pytest


@pytest.mark.parametrize('session_name, exception', [
    ('', EnvAssumeException),
    ('\'', EnvAssumeException),
])
def test_session_name_constraints_exceptions(session_name, exception):
    with pytest.raises(exception):
        apply_session_name_constraints(session_name)


@pytest.mark.parametrize('session_name, expected_session_name', [
    ('0123456789', '0123456789'),
    ('*0123456789', '0123456789'),
    ('0*123456789', '0123456789'),
    ('0123456789*', '0123456789'),
    (
        '0123456789012345678901234567890123456789012345678901234567890123456789',
        '0123456789012345678901234567890123456789012345678901234567890123',
    ),
])
def test_session_name_constraints(session_name, expected_session_name):
    assert expected_session_name == apply_session_name_constraints(session_name)

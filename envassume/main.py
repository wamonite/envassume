# -*- coding: utf-8 -*-
"""
envassume
"""

from __future__ import print_function
import sys
import os
from socket import gethostname
import boto3


class EnvAssumeException(Exception):
    pass


def pop_argument(arg_list):
    try:
        return arg_list.pop(0)

    except IndexError:
        raise EnvAssumeException('Not enough arguments')


def parse_arguments(arg_list):
    pop_argument(arg_list)

    external_id = None
    if arg_list[0] in ('-i', '--external-id'):
        pop_argument(arg_list)
        external_id = pop_argument(arg_list)

    role_arn = os.environ.get('AWS_ASSUME_ROLE')
    if not role_arn:
        role_arn = pop_argument(arg_list)

    if arg_list[0] == '--':
        pop_argument(arg_list)

    return role_arn, external_id, arg_list


def assume_role(role_arn, external_id = None, session_name = None):
    if not external_id:
        external_id = os.environ.get('AWS_EXTERNAL_ID')

    if not session_name:
        session_name = 'envassume-' + gethostname()

    request = {
        'RoleArn': role_arn,
        'RoleSessionName': session_name
    }

    if external_id:
        request['ExternalId'] = external_id

    boto3_session = boto3.Session()
    sts_client = boto3_session.client('sts')
    response = sts_client.assume_role(**request)

    return response.get('Credentials') or {}


def update_env(credentials_lookup):
    credentials_list = (
        ('AccessKeyId', 'AWS_ACCESS_KEY_ID'),
        ('SecretAccessKey', 'AWS_SECRET_ACCESS_KEY'),
        ('SessionToken', 'AWS_SESSION_TOKEN'),
    )
    for credential_key, env_var_name in credentials_list:
        os.environ[env_var_name] = credentials_lookup[credential_key]


def run_command(arg_list):
    try:
        os.execvpe(arg_list[0], arg_list, os.environ)

    except OSError as e:
        raise EnvAssumeException('Unable to run command {}: {}'.format(arg_list[0], e))

    raise EnvAssumeException('Unable to run command {}'.format(arg_list[0]))


def run():
    role_arn, external_id, arg_list = parse_arguments(sys.argv)

    credentials_lookup = assume_role(role_arn, external_id)

    update_env(credentials_lookup)

    run_command(arg_list)


def run_script():
    try:
        run()

    except Exception as e:
        print('Error({}) {}'.format(e.__class__.__name__, e), file = sys.stderr)
        sys.exit(1)

    except KeyboardInterrupt:
        pass

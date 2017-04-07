#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
envassume
"""

from __future__ import print_function
import sys
import os
from socket import gethostname
import boto3
import subprocess


class EnvAssumeException(Exception):
    pass


def parse_arguments(arg_list):
    role_arn = os.environ.get('AWS_ASSUME_ROLE')
    if role_arn:
        if len(sys.argv) <= 1:
            raise EnvAssumeException('no command supplied')

        command_list = arg_list[1:]

    else:
        if len(sys.argv) <= 2:
            raise EnvAssumeException('not enough arguments')

        role_arn = arg_list[1]
        command_list = arg_list[2:]

    return role_arn, command_list


def assume_role(role_arn, external_id = None, session_name = None):
    if not external_id:
        external_id = os.environ.get('AWS_EXTERNAL_ID')

    if not session_name:
        session_name = 'env_assume-' + gethostname()

    request = {
        'RoleArn': role_arn,
        'RoleSessionName': session_name
    }

    if external_id:
        request['ExternalId'] = external_id

    boto3_session = boto3.Session()
    sts_client = boto3_session.client('sts')
    response = sts_client.assume_role(**request)

    return response.get('Credentials')


def update_env(credentials_lookup):
    credentials_list = (
        ('AccessKeyId', 'AWS_ACCESS_KEY_ID'),
        ('SecretAccessKey', 'AWS_SECRET_ACCESS_KEY'),
        ('SessionToken', 'AWS_SESSION_TOKEN'),
    )
    for credential_key, env_var_name in credentials_list:
        os.environ[env_var_name] = credentials_lookup[credential_key]


def run_command(command_list):
    try:
        subprocess.check_call(command_list)

    except subprocess.CalledProcessError as e:
        return e.returncode

    return 0


def run():
    role_arn, command_list = parse_arguments(sys.argv)

    credentials_lookup = assume_role(role_arn)

    update_env(credentials_lookup)

    return run_command(command_list)


def run_script():
    try:
        exit_code = run()
        sys.exit(exit_code)

    except Exception as e:
        print('Error({}) {}'.format(e.__class__.__name__, e), file = sys.stderr)
        sys.exit(1)

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    run_script()

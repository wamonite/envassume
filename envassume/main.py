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


class ScriptException(Exception):
    pass


def do_env_assume():
    role_arn = os.environ.get('AWS_ASSUME_ROLE')
    if role_arn:
        if len(sys.argv) <= 1:
            raise ScriptException('no command supplied')

        cmd_list = sys.argv[1:]

    else:
        if len(sys.argv) <= 2:
            raise ScriptException('not enough arguments')

        role_arn = sys.argv[1]
        cmd_list = sys.argv[2:]

    request = {
        'RoleArn': role_arn,
        'RoleSessionName': 'env_assume-' + gethostname()
    }

    external_id = os.environ.get('AWS_EXTERNAL_ID')
    if external_id:
        request['ExternalId'] = external_id

    boto_session = boto3.Session()
    sts_client = boto_session.client('sts')
    response = sts_client.assume_role(**request)

    credentials = response.get('Credentials')
    credentials_list = (
        ('AccessKeyId', 'AWS_ACCESS_KEY_ID'),
        ('SecretAccessKey', 'AWS_SECRET_ACCESS_KEY'),
        ('SessionToken', 'AWS_SESSION_TOKEN'),
    )
    for credential_key, env_var_name in credentials_list:
        os.environ[env_var_name] = credentials[credential_key]

    subprocess.check_call(cmd_list)


if __name__ == "__main__":
    try:
        do_env_assume()

    except Exception as e:
        print('Error:{}: {}'.format(e.__class__.__name__, e), file = sys.stderr)
        sys.exit(1)

    except KeyboardInterrupt:
        pass

envassume
=========

Assume an AWS IAM role from environment variables.

Usage
-----

::

    usage: envassume [-h] [-i EXTERNAL_ID] [ARN] command [argument [argument ...]]

    positional arguments:

        command                 command to run
        argument                command arguments

    optional arguments:
        -h, --help              show this help message and exit
        -i, --id EXTERNAL_ID    external id
        ARN                     ARN to assume (if not set by environment variable)

Environment Variables
---------------------

* `AWS_ASSUME_ROLE=ARN`
    `ARN` and options cannot be set if this is defined
* `AWS_ASSUME_ID=EXTERNAL_ID`
    external id

License
-------

Copyright (c) 2017 Warren Moore

This software may be redistributed under the terms of the MIT License.
See the file LICENSE for details.

Contact
-------

::

          @wamonite     - twitter
           \_______.com - web
    warren____________/ - email

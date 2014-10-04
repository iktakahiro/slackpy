slackpy
=======

slackpy is `Slack`_ client library for specific logging.

Install
-------

.. code:: python

    pip install slackpy

Dependencies
------------

-  requests

Sample Code
-----------

.. code:: python

    import slackpy

    AUTH_TOKEN = 'your_api_token'
    CHANNEL = '#your_channel'
    USER_NAME = 'Logger'

    # Create a new instance.
    logging = slackpy.SlackLogger(AUTH_TOKEN, CHANNEL, USER_NAME)

    # LogLevel: INFO
    logging.info(message='INFO Message')

    # LogLevel: WARN
    logging.warn(message='WARN Message')

    # LogLevel: ERROR
    logging.error(message='ERROR Message')

Correspondence table
~~~~~~~~~~~~~~~~~~~~

+-----------+---------------+--------------------+
| Method    | LogLevel      | Color              |
+===========+===============+====================+
| info()    | INFO (1)      | good (green)       |
+-----------+---------------+--------------------+
| warn()    | WARNING (2)   | warning (orange)   |
+-----------+---------------+--------------------+
| error()   | ERROR (3)     | danger (red)       |
+-----------+---------------+--------------------+

Command line
------------

.. code:: sh

    export SLACK_TOKEN=your_api_token

    # LogLevel: INFO
    slackpy -c 'your_channel' -m 'INFO Message' -l 1

    # LogLevel: WARN
    slackpy -c 'your_channel' -m 'WARN Message' -l 2

    # LogLevel: ERROR
    slackpy -c 'your_channel' -m 'ERROR Message' -l 3

    # LogLevel: INFO (with Message Title)
    slackpy -c 'your_channel' -t 'Message Title' -m 'INFO Message' -l 1

.. _Slack: https://slack.com


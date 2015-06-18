slackpy
=======

slackpy is `Slack`_ client library for specific logging.

Install
-------

.. code:: sh

    pip install slackpy

Dependencies
------------

-  requests 2.7

Sample Code
-----------

.. code:: python

    import slackpy

    INCOMING_WEB_HOOK = 'your_web_hook_url'
    CHANNEL = '#general'
    USER_NAME = 'Logger'

    # Create a new instance.
    logging = slackpy.SlackLogger(INCOMING_WEB_HOOK, CHANNEL, USER_NAME)

    # LogLevel: INFO
    logging.info(message='INFO Message')

    # LogLevel: WARN
    logging.warn(message='WARN Message')

    # LogLevel: ERROR
    logging.error(message='ERROR Message')

Correspondence table
~~~~~~~~~~~~~~~~~~~~

+-----------+---------------+----------------------+
| Method    | LogLevel      | Color                |
+===========+===============+======================+
| info()    | DEBUG (10)    | #03A9F4 (Light Blue) |
+-----------+---------------+----------------------+
| info()    | INFO (20)     | good (green)         |
+-----------+---------------+----------------------+
| warn()    | WARNING (30)  | warning (orange)     |
+-----------+---------------+----------------------+
| error()   | ERROR (40)    | danger (red)         |
+-----------+---------------+----------------------+

Command line
------------

.. code:: sh

    export SLACK_INCOMING_WEB_HOOK='your_web_hook_url'

    # LogLevel: DEBUG
    slackpy -c '#your_channel' -m 'DEBUG Message' -l 10

    # LogLevel: INFO
    slackpy -c '#your_channel' -m 'INFO Message' -l 20

    # LogLevel: WARN
    slackpy -c '#your_channel' -m 'WARN Message' -l 30

    # LogLevel: ERROR
    slackpy -c '#your_channel' -m 'ERROR Message' -l 40

    # LogLevel: INFO (with Message Title)
    slackpy -c '#your_channel' -t 'Message Title' -m 'INFO Message' -l 20

.. _Slack: https://slack.com


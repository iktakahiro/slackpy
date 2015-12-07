|Build Status|

slackpy
=======

slackpy is `Slack`_ client library for specific logging.

Install
-------

.. code:: sh

    pip install slackpy

Dependencies
------------

-  requests<3,>=2.8.0

Sample Code
-----------

.. code:: python

    import slackpy

    INCOMING_WEB_HOOK = 'your_web_hook_url'
    CHANNEL = '#general'
    USER_NAME = 'Logger'

    # Create a new instance.
    logging = slackpy.SlackLogger(INCOMING_WEB_HOOK, CHANNEL, USER_NAME)

    # You can set log level. Default level is INFO.
    logging.set_log_level(slackpy.LogLv.DEBUG) # Or logging.set_log_level(10)

    ## Minimum Parameter
    ## logging = slackpy.SlackLogger(INCOMING_WEB_HOOK)

    LogLevel's only required parameter is "message", all others are optional.

    # LogLevel: DEBUG
    logging.info(message='INFO Message', title='INFO Title', fallback='', fields='')

    # LogLevel: INFO
    logging.info(message='INFO Message', title='INFO Title', fallback='', fields='')

    # LogLevel: WARN
    logging.warn(message='WARN Message', title='INFO Title', fallback='', fields='')

    # LogLevel: ERROR
    logging.error(message='ERROR Message', title='INFO Title', fallback='', fields='')

    # LogLevel: CUSTOM
    logging.message(message='CUSTOM Message', title='CUSTOM Title', fallback='CUSTOM Fallback', color='good',
                    fields=[{"title": "CUSTOM", "value": "test", "short": "true"}],
                    log_level=40)

Correspondence table
~~~~~~~~~~~~~~~~~~~~

+-----------+----------------+------------------------+
| Method    | LogLevel       | Color                  |
+===========+================+========================+
| debug()   | DEBUG (10)     | #03A9F4 (Light Blue)   |
+-----------+----------------+------------------------+
| info()    | INFO (20)      | good (green)           |
+-----------+----------------+------------------------+
| warn()    | WARNING (30)   | warning (orange)       |
+-----------+----------------+------------------------+
| error()   | ERROR (40)     | danger (red)           |
+-----------+----------------+------------------------+

LogLevel based on logging standard library
(https://docs.python.org/3.4/library/logging.html#levels)

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

    # LogLevel: DEBUG (without specifying #channel)
    slackpy -m 'DEBUG Message' -l 10

    # LogLevel: INFO (with Message Title)
    slackpy -c '#your_channel' -t 'DEBUG: Message Title' -m 'INFO Message' -l 20

.. _Slack: https://slack.com

.. |Build Status| image:: https://travis-ci.org/iktakahiro/slackpy.svg
   :target: https://travis-ci.org/iktakahiro/slackpy

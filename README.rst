.. image:: https://img.shields.io/pypi/v/slackpy.svg
    :target: https://pypi.python.org/pypi/slackpy

.. image:: https://img.shields.io/pypi/dm/slackpy.svg
    :target: https://pypi.python.org/pypi/slackpy

.. image:: https://travis-ci.org/iktakahiro/slackpy.svg?branch=master
    :target: https://travis-ci.org/iktakahiro/slackpy

slackpy
=======

slackpy is simple and useful `Slack`_ client library for logging.

Use Case
--------

- Web Application
- NEW! `AWS Lambda`_
- Bash Script

Install
-------

.. code:: sh

    pip install slackpy

Dependencies
------------

-  requests

Sample Code
-----------

.. code:: python

    import slackpy

    INCOMING_WEB_HOOK = 'your_web_hook_url'
    CHANNEL = '#general'
    USER_NAME = 'Logger'
    ICON_URL = 'http://lorempixel.com/48/48'

    # Create a new instance.
    logging = slackpy.SlackLogger(INCOMING_WEB_HOOK, CHANNEL, USER_NAME, ICON_URL)

    # You can set a log level. Default level is INFO.
    logging.set_log_level(slackpy.LogLv.DEBUG) # Or logging.set_log_level(10)

    ## Minimum Parameter
    ## logging = slackpy.SlackLogger(INCOMING_WEB_HOOK)

    # Simple Usage
    logging.info('INFO Message')

    # LogLevel's only required parameter is "message", all others are optional.

    # LogLevel: DEBUG
    logging.debug(message='DEBUG Message', title='DEBUG Title', fields='')

    # LogLevel: INFO
    logging.info(message='INFO Message', title='INFO Title', fields='')

    # LogLevel: WARN
    logging.warn(message='WARN Message', title='WARN Title', fields='')

    # LogLevel: ERROR
    logging.error(message='ERROR Message', title='ERROR Title', fields='')

    # LogLevel: CUSTOM
    logging.message(message='CUSTOM Message', title='CUSTOM Title', color='good',
                    fields=[{"title": "CUSTOM", "value": "test", "short": True}],
                    log_level=40)

    # Title Link (New v2.1.0)
    logging.info(message='INFO Message', title='slackpy Repository here',
                 title_link='https://github.com/iktakahiro/slackpy')

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
    slackpy -c '#your_channel' -t 'INFO Message Title' -m 'INFO Message' -l 20

For AWS Lamdba
--------------

.. code:: sh

   # First, pip install to top of project directory.
   pip install slackpy -t .

   # Second, Archive your source code and dependency packages.
   zip -r src.zip lambda_function.py slackpy enum requests

   # Finally, Upload your src.zip

About Versioning
----------------

slackpy is following `Semantic Versioning 2.0.0 <http://semver.org/spec/v2.0.0.html>`_.

.. _Slack: https://slack.com

.. _AWS Lambda: https://aws.amazon.com/lambda/


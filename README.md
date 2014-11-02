# slackpy

slackpy is [Slack][] client library for specific logging.

## Install

```sh
pip install slackpy
```

## Dependencies

-   requests 2.3.4

## Sample Code

```python
import slackpy

SUB_DOMAIN = 'your_sub_domain' # if your domain is test.slack.com, input 'test'.
AUTH_TOKEN = 'your_web_hook_token'
CHANNEL = '#general'
USER_NAME = 'Logger'

# Create a new instance.
logging = slackpy.SlackLogger(SUB_DOMAIN, AUTH_TOKEN, CHANNEL, USER_NAME)

# LogLevel: INFO
logging.info(message='INFO Message')

# LogLevel: WARN
logging.warn(message='WARN Message')

# LogLevel: ERROR
logging.error(message='ERROR Message')
```

### Correspondence table

  Method     LogLevel       Notify    Color
  ---------- -------------- --------- ---------
  info()     INFO (1)       False     green
  warn()     WARNING (2)    True      yellow
  error()    ERROR (3)      True      red

## Command line

```sh
export SLACK_SUB_DOMAIN=your_sub_domain # if your domain is test.slack.com, input 'test'.
export SLACK_WEB_HOOK_TOKEN=your_web_hook_token

# LogLevel: INFO
slackpy -c '#your_channel' -m 'INFO Message' -l 1

# LogLevel: WARN
slackpy -c '#your_channel' -m 'WARN Message' -l 2

# LogLevel: ERROR
slackpy -c '#your_channel' -m 'ERROR Message' -l 3

# LogLevel: INFO (with Message Title)
slackpy -c '#your_channel' -t 'Message Title' -m 'INFO Message' -l 1
```

  [Slack]: https://slack.com

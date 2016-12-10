#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from slackpy import SlackLogger, LogLv, LOG_LEVELS
from argparse import ArgumentParser

__author__ = 'Takahiro Ikeuchi'


def main():
    parser = ArgumentParser(description='slackpy command line tool')
    parser.add_argument('-m',
                        '--message',
                        type=str,
                        required=True,
                        help='Message body.')
    parser.add_argument('-c',
                        '--channel',
                        required=False,
                        help='Slack Channel. channel must be started with # or @',
                        default=None)
    parser.add_argument('-t',
                        '--title',
                        type=str,
                        required=False,
                        help='Message title.',
                        default='Slack Notification')
    parser.add_argument('-n',
                        '--name',
                        type=str,
                        required=False,
                        help='Your bot\'s user name',
                        default='Logger')

    # The purpose of backward compatibility, old args (1, 2, 3)
    # are being retained.
    # DEBUG == 10, INFO == 20, # WARNING == 30, ERROR == 40
    parser.add_argument('-l',
                        '--level',
                        type=int,
                        default=20,
                        choices=LOG_LEVELS.append([1, 2, 3]))

    args = parser.parse_args()

    try:
        web_hook_url = os.environ["SLACK_INCOMING_WEB_HOOK"]

    except KeyError:
        print('ERROR: Please set a SLACK_INCOMING_WEB_HOOK variable in ' +
              'your environment.')
    else:

        client = SlackLogger(web_hook_url, args.channel, args.name)

        # Command Line mode can use only DEBUG level.
        client.set_log_level(LogLv.DEBUG)

        if args.level == LogLv.DEBUG:
            response = client.debug(args.message, args.title)

        elif args.level == LogLv.INFO:
            response = client.info(args.message, args.title)

        elif args.level == LogLv.WARN:
            response = client.warn(args.message, args.title)

        elif args.level == LogLv.ERROR:
            response = client.error(args.message, args.title)

        else:
            raise Exception("'Level' must be selected from among 10 to 40")

        if response.status_code == 200:
            print(True)

        else:
            print(False)

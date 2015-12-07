#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from slackpy import SlackLogger, LogLv, LOG_LEVELS
from argparse import ArgumentParser

__author__ = 'Takahiro Ikeuchi'


def main():
    try:
        web_hook_url = os.environ["SLACK_INCOMING_WEB_HOOK"]

    except KeyError:
        print('ERROR: Please set the SLACK_INCOMING_WEB_HOOK variable in ' +
              ' your environment.')

    else:
        parser = ArgumentParser(description='slackpy command line tool')
        parser.add_argument('-m',
                            '--message',
                            type=str,
                            required=True,
                            help='Message')
        parser.add_argument('-c',
                            '--channel',
                            required=False,
                            help='Channel',
                            default=None)
        parser.add_argument('-t',
                            '--title',
                            type=str,
                            required=False,
                            help='Title',
                            default='Slack Notification')
        parser.add_argument('-n',
                            '--name',
                            type=str,
                            required=False,
                            help='Name of Postman',
                            default='Logger')
        parser.add_argument('-f',
                            '--fallback',
                            type=str,
                            required=False,
                            help='A plain-text summary of the attachment',
                            default='')

        # The purpose of backward compatibility, old args (1, 2, 3)
        # are being retained.
        # DEBUG == 10, INFO == 20, # WARNING == 30, ERROR == 40
        parser.add_argument('-l',
                            '--level',
                            type=int,
                            default=20,
                            choices=LOG_LEVELS.append([1, 2, 3]))

        args = parser.parse_args()

        client = SlackLogger(web_hook_url, args.channel, args.name)

        # Command Line mode can use only DEBUG level.
        client.set_log_level(LogLv.DEBUG)

        if args.level == LogLv.DEBUG:
            response = client.debug(args.message, args.title, args.fallback)

        elif args.level == LogLv.INFO or args.level == 1:
            response = client.info(args.message, args.title, args.fallback)

        elif args.level == LogLv.WARN or args.level == 2:
            response = client.warn(args.message, args.title, args.fallback)

        elif args.level == LogLv.ERROR or args.level == 3:
            response = client.error(args.message, args.title, args.fallback)

        else:
            raise Exception("'Level' must be selected from among 1 to 3")

        if response.status_code == 200:
            print(True)

        else:
            print(False)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Takahiro Ikeuchi'

import os
import requests
import json
import traceback
from argparse import ArgumentParser


class SlackLogger:
    def __init__(self, web_hook_url, channel, username='Logger'):

        self.web_hook_url = web_hook_url
        self.channel = channel
        self.username = username

        if channel.startswith('#') or channel.startswith('@'):
            pass

        else:
            raise ValueError('channel must be started with "#" or "@".')

    def __build_payload(self, message, title, color):

        __fields = {
            "title": title,
            "text": message,
            "color": color,
            "fallback": title,
        }

        __attachments = {
            "fields": __fields
        }

        payload = {
            "channel": self.channel,
            "username": self.username,
            "attachments": __attachments
        }

        return payload

    def __send_notification(self, message, title, color='good'):
        """Send a message to a channel.
        Args:
            title: The message title.
            message: The message body.
            color: Can either be one of 'good', 'warning', 'danger', or any hex color code

        Returns:
            api_response:

        Raises:
            TODO:
        """
        payload = self.__build_payload(message, title, color)

        try:
            response = requests.post(self.web_hook_url, data=json.dumps(payload))

        except Exception:
            raise Exception(traceback.format_exc())

        else:
            if response.status_code == 200:
                return response

            else:
                raise Exception(response.content.decode())

    def debug(self, message, title='Slack Notification'):
        title = 'DEBUG : {0}'.format(title)
        return self.__send_notification(message=message, title=title, color='#03A9F4')

    def info(self, message, title='Slack Notification'):
        title = 'INFO : {0}'.format(title)
        return self.__send_notification(message=message, title=title, color='good')

    def warn(self, message, title='Slack Notification'):
        title = 'WARN : {0}'.format(title)
        return self.__send_notification(message=message, title=title, color='warning')

    def error(self, message, title='Slack Notification'):
        title = 'ERROR : {0}'.format(title)
        return self.__send_notification(message=message, title=title, color='danger')


def main():
    try:
        web_hook_url = os.environ["SLACK_INCOMING_WEB_HOOK"]

    except KeyError:
        print('ERROR: Please set the SLACK_INCOMING_WEB_HOOK variable in your environment.')

    else:
        parser = ArgumentParser(description='slackpy command line tool')
        parser.add_argument('-c', '--channel', required=True, help='Channel')
        parser.add_argument('-m', '--message', type=str, required=True, help='Message')
        parser.add_argument('-t', '--title', type=str, required=False, help='Title', default='Slack Notification')
        parser.add_argument('-n', '--name', type=str, required=False, help='Name of Postman', default='Logger')

        # The purpose of backward compatibility, old args (1, 2, 3) are being retained.
        # DEBUG == 10, INFO == 20, # WARNING == 30, ERROR == 40
        parser.add_argument('-l', '--level', type=int, default=20, choices=[10, 20, 30, 40, 1, 2, 3])

        args = parser.parse_args()

        client = SlackLogger(web_hook_url, args.channel, args.name)

        if args.level == 10:
            response = client.debug(args.message, args.title)

        elif args.level == 20 or args.level == 1:
            response = client.info(args.message, args.title)

        elif args.level == 30 or args.level == 2:
            response = client.warn(args.message, args.title)

        elif args.level == 40 or args.level == 3:
            response = client.error(args.message, args.title)

        else:
            raise Exception("'Level' must be selected from among 1 to 3")

        if response.status_code == 200:
            print(True)

        else:
            print(False)


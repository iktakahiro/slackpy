#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Takahiro Ikeuchi'

import os
import requests
import json
from argparse import ArgumentParser


class SlackLogger:
    def __init__(self, web_hook_url, channel, username='Logger'):

        self.web_hook_url = web_hook_url
        self.channel = channel
        self.username = username

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

        response = requests.post(self.web_hook_url, data=json.dumps(payload))

        return response

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
        parser.add_argument('-l', '--level', type=int, default=1, choices=[1, 2, 3])

        args = parser.parse_args()

        client = SlackLogger(web_hook_url, args.channel, args.name)

        if args.level == 1:
            response = client.info(args.message, args.title)

        if args.level == 2:
            response = client.warn(args.message, args.title)

        if args.level == 3:
            response = client.error(args.message, args.title)

        if response.status_code == 200:
            print(True)

        else:
            print(False)


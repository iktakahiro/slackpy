#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Takahiro Ikeuchi'

import os
import requests
import json
import traceback
from argparse import ArgumentParser


class SlackLogger:
    def __init__(self, web_hook_url, channel=None, username='Logger'):

        self.web_hook_url = web_hook_url
        self.username = username

        if channel is None:
            self.channel = None

        elif channel.startswith('#') or channel.startswith('@'):
            self.channel = channel

        else:
            raise ValueError('channel must be started with "#" or "@".')

    def __build_payload(self, message, title, color, fallback, fields):

        if fields is '':
            __fields = {
                "title": title,
                "text": message,
                "color": color,
                "fallback": fallback
            }

            __attachments = {
                "fields": __fields
            }
        else:
            __attachments = [{
                "fallback": fallback,
                "color": color,
                "text": message,
                "fields": fields
            }]

        payload = {
            "channel": self.channel,
            "username": self.username,
            "attachments": __attachments
        }

        return payload

    def __send_notification(self, message, title, color='good', fallback='',
                            fields=''):
        """Send a message to a channel.
        Args:
            title: The message title.
            message: The message body.
            color: Can either be one of 'good', 'warning', 'danger',
                   or any hex color code
            fallback: What is shown to IRC/fallback clients

        Returns:
            api_response:

        Raises:
            TODO:
        """
        if fallback is '':
            fallback = title

        payload = self.__build_payload(message, title, color, fallback, fields)

        try:
            response = requests.post(self.web_hook_url,
                                     data=json.dumps(payload))

        except Exception:
            raise Exception(traceback.format_exc())

        else:
            if response.status_code == 200:
                return response

            else:
                raise Exception(response.content.decode())

    def debug(self, message, title='Slack Notification', fallback='',
              fields=''):
        return self.__send_notification(message=message,
                                        title=title,
                                        color='#03A9F4',
                                        fallback=fallback,
                                        fields=fields)

    def info(self, message, title='Slack Notification', fallback='',
             fields=''):
        return self.__send_notification(message=message,
                                        title=title,
                                        color='good',
                                        fallback=fallback,
                                        fields=fields)

    def warn(self, message, title='Slack Notification', fallback='',
             fields=''):
        return self.__send_notification(message=message,
                                        title=title,
                                        color='warning',
                                        fallback=fallback,
                                        fields=fields)

    def error(self, message, title='Slack Notification', fallback='',
              fields=''):
        return self.__send_notification(message=message,
                                        title=title,
                                        color='danger',
                                        fallback=fallback,
                                        fields=fields)

    def message(self, message, title='Slack Notification', fallback='',
                color='good', fields=''):
        return self.__send_notification(message=message,
                                        title=title,
                                        color=color,
                                        fallback=fallback,
                                        fields=fields)


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
                            choices=[10, 20, 30, 40, 1, 2, 3])

        args = parser.parse_args()

        client = SlackLogger(web_hook_url, args.channel, args.name)

        if args.level == 10:
            response = client.debug(args.message, args.title, args.fallback)

        elif args.level == 20 or args.level == 1:
            response = client.info(args.message, args.title, args.fallback)

        elif args.level == 30 or args.level == 2:
            response = client.warn(args.message, args.title, args.fallback)

        elif args.level == 40 or args.level == 3:
            response = client.error(args.message, args.title, args.fallback)

        else:
            raise Exception("'Level' must be selected from among 1 to 3")

        if response.status_code == 200:
            print(True)

        else:
            print(False)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import json
import traceback
import requests
from enum import IntEnum, unique

__author__ = 'Takahiro Ikeuchi'


@unique
class LogLv(IntEnum):
    DEBUG = 10
    INFO = 20
    WARN = 30
    ERROR = 40


LOG_LEVELS = list(map(int, LogLv))


class SlackLogger:
    def __init__(self, web_hook_url, channel=None, username='Logger'):

        self.web_hook_url = web_hook_url
        self.username = username
        self.log_level = LogLv.INFO

        if channel is None:
            self.channel = None

        elif channel.startswith('#') or channel.startswith('@'):
            self.channel = channel

        else:
            raise ValueError('channel must be started with "#" or "@".')

    def set_log_level(self, lv):

        if lv in LOG_LEVELS:
            self.log_level = lv

        else:
            raise ValueError('argument lv is invalid. Choose from values in ErrorLv Class.')

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
                            fields='', log_level=LogLv.INFO):
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
        if log_level < self.log_level:
            return None

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
                                        fields=fields,
                                        log_level=LogLv.DEBUG)

    def info(self, message, title='Slack Notification', fallback='',
             fields=''):
        return self.__send_notification(message=message,
                                        title=title,
                                        color='good',
                                        fallback=fallback,
                                        fields=fields,
                                        log_level=LogLv.INFO)

    def warn(self, message, title='Slack Notification', fallback='',
             fields=''):
        return self.__send_notification(message=message,
                                        title=title,
                                        color='warning',
                                        fallback=fallback,
                                        fields=fields,
                                        log_level=LogLv.WARN)

    def error(self, message, title='Slack Notification', fallback='',
              fields=''):
        return self.__send_notification(message=message,
                                        title=title,
                                        color='danger',
                                        fallback=fallback,
                                        fields=fields,
                                        log_level=LogLv.ERROR)

    def message(self, message, title='Slack Notification', fallback='',
                color='good', fields='', log_level=LogLv.ERROR):
        return self.__send_notification(message=message,
                                        title=title,
                                        color=color,
                                        fallback=fallback,
                                        fields=fields,
                                        log_level=log_level)

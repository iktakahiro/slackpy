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

    def __build_payload(self, message, title, title_link, color, fields):

        __attachments = [{
            'title': title,
            'title_link': title_link,
            'color': color,
            'text': message,
            'fields': fields,
            'mrkdwn_in': ['text', 'fields', 'title']
        }]

        payload = {
            'channel': self.channel,
            'username': self.username,
            'attachments': __attachments,
        }

        return payload

    def __send_notification(self, message, title, title_link='', color='good',
                            fields='', log_level=LogLv.INFO):
        """Send a message to a channel.
        Args:
            title: A message title.
            title: A link of the message title.
            message: The message body.
            color: Can either be one of 'good', 'warning', 'danger',
                   or any hex color code.

        Returns:
            response: A Response of Slack API.

        Raises:
            Exception:
        """
        if log_level < self.log_level:
            return None

        payload = self.__build_payload(message, title, title_link, color, fields)

        try:
            response = requests.post(self.web_hook_url,
                                     data=json.dumps(payload), timeout=3, allow_redirects=False)

        except Exception:
            raise Exception(traceback.format_exc())

        else:
            if response.status_code == 200:
                return response

            else:
                raise Exception('POST failed.')

    def debug(self, message, title='Slack Notification', title_link='', fields=''):
        return self.__send_notification(message=message,
                                        title=title,
                                        title_link=title_link,
                                        color='#03A9F4',
                                        fields=fields,
                                        log_level=LogLv.DEBUG)

    def info(self, message, title='Slack Notification', title_link='', fields=''):
        return self.__send_notification(message=message,
                                        title=title,
                                        title_link=title_link,
                                        color='good',
                                        fields=fields,
                                        log_level=LogLv.INFO)

    def warn(self, message, title='Slack Notification', title_link='', fields=''):
        return self.__send_notification(message=message,
                                        title=title,
                                        title_link=title_link,
                                        color='warning',
                                        fields=fields,
                                        log_level=LogLv.WARN)

    def error(self, message, title='Slack Notification', title_link='', fields=''):
        return self.__send_notification(message=message,
                                        title=title,
                                        title_link=title_link,
                                        color='danger',
                                        fields=fields,
                                        log_level=LogLv.ERROR)

    def message(self, message, title='Slack Notification', title_link='', color='good', fields='',
                log_level=LogLv.ERROR):
        return self.__send_notification(message=message,
                                        title=title,
                                        title_link=title_link,
                                        color=color,
                                        fields=fields,
                                        log_level=log_level)

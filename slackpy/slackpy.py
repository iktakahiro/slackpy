#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Takahiro Ikeuchi'

import os
import requests
import json
from argparse import ArgumentParser
from copy import deepcopy


class HipChatLogger:
    def __init__(self, auth_token, room_id, base_uri='https://api.hipchat.com/v2/', response_format='json',
                 http_proxy='', https_proxy=''):

        self.auth_token = auth_token
        self.room_id = room_id
        self.base_uri = base_uri
        self.response_format = response_format
        self.http_proxy = http_proxy
        self.https_proxy = https_proxy

    def __post(self, post_params, endpoint):
        """POST HTTP Request.

        Args:
            post_params:
            endpoint:

        Returns:
            response:

        Raises:
            TODO:

        """
        __post_params = deepcopy(post_params)

        headers = {'content-type': 'application/json'}

        proxy_dict = {}
        if self.http_proxy:
            proxy_dict['http'] = self.http_proxy
        if self.https_proxy:
            proxy_dict['https'] = self.https_proxy

        uri = self.base_uri + endpoint + '?auth_token=' + self.auth_token

        if not proxy_dict:
            proxy_dict = None

        http = requests.session()
        response = http.post(uri, data=json.dumps(__post_params), headers=headers, proxies=proxy_dict)
        http.close()

        return response

    def __send_notification(self, message, message_format='html', notify=False, color='yellow'):
        """Send a message to a room.

        Args:
            message: The message body. 10,000 characters max.
            message_format: Determines how the message is treated by our server and rendered inside HipChat applications.
            notify: Whether or not this message should trigger a notification for people in the room.
            color: Background color for message.
                   One of "yellow", "red", "green", "purple", "gray", or "random". (default: yellow)

        Returns:
            response:

        Raises:
            TODO:

        """

        params = {
            "message": message,
            "message_format": message_format,
            "notify": notify,
            "color": color
        }

        endpoint = 'room/' + str(self.room_id) + '/notification'

        response = self.__post(params, endpoint)

        return response.status_code

    def info(self, message, message_format='html'):

        return self.__send_notification(message=message, message_format=message_format, notify=False, color='green')

    def warn(self, message, message_format='html'):

        return self.__send_notification(message=message, message_format=message_format, notify=True, color='yellow')

    def error(self, message, message_format='html'):

        return self.__send_notification(message=message, message_format=message_format, notify=True, color='red')


def main():
    try:
        auth_token = os.environ["HIPCHAT_TOKEN"]

    except KeyError:
        print('ERROR: Please set the HIPCHAT_TOKEN variable in your environment.')

    else:
        parser = ArgumentParser(description='hipchatpy command line tool')
        parser.add_argument('-r', '--room', required=True, help='Room ID')
        parser.add_argument('-m', '--message', type=str, required=True, help='Message')
        parser.add_argument('-l', '--level', type=int, default=1, choices=[1, 2, 3])
        parser.add_argument('-f', '--format', type=str, default='html', choices=['html', 'text'])

        args = parser.parse_args()

        client = HipChatLogger(auth_token, args.room)

        if args.level == 1:
            response = client.info(args.message, message_format=args.format)

        if args.level == 2:
            response = client.warn(args.message, message_format=args.format)

        if args.level == 3:
            response = client.error(args.message, message_format=args.format)

        if response == 204:
            print(True)

        else:
            print(False)


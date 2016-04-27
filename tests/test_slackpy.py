#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pytest
from slackpy.slackpy import SlackLogger, LOG_LEVELS, LogLv

__author__ = 'Takahiro Ikeuchi'

DUMMY_WEB_HOOK = 'http://dummy_url'

try:
    VALID_WEB_HOOK = os.environ["SLACK_INCOMING_TEST_WEB_HOOK"]

except KeyError:
    print('ERROR: Please set a SLACK_INCOMING_TEST_WEB_HOOK variable in ' +
          'your environment.')


class TestSlackLogger:
    def test_channel_value_error(self):
        with pytest.raises(ValueError):
            SlackLogger(DUMMY_WEB_HOOK, 'dummy_channel', 'Test User')

    def test_build_payload_with_all_parameters(self):
        logger = SlackLogger(DUMMY_WEB_HOOK, '#dummy_channel', 'Test User')
        actual = logger._SlackLogger__build_payload('Test Message',
                                                    'Test Title',
                                                    'Color Name',
                                                    '')

        expected = {
            "channel": "#dummy_channel",
            "username": "Test User",
            "attachments": [
                {'color': 'Color Name',
                 'text': 'Test Message',
                 "title": "Test Title",
                 'mrkdwn_in': ['text', 'fields', 'title'],
                 "fields": '',
                 }]
        }

        assert expected == actual

    def test_build_payload_without_specifying_optional_parameters(self):
        logger = SlackLogger(DUMMY_WEB_HOOK)
        actual = logger._SlackLogger__build_payload('Test Message',
                                                    'Test Title',
                                                    'Color Name',
                                                    '')

        expected = {
            "channel": None,
            "username": "Logger",
            "attachments": [
                {'color': 'Color Name',
                 'text': 'Test Message',
                 "title": "Test Title",
                 'mrkdwn_in': ['text', 'fields', 'title'],
                 "fields": '',
                 }]
        }

        assert expected == actual

    def test_build_payload_with_custom_fields(self):
        logger = SlackLogger(DUMMY_WEB_HOOK, '#dummy_channel', 'Test User')

        test_fields = list()
        test_fields.append({
            "title": "Project",
            "value": "Test Project",
            "short": "true"
        })
        test_fields.append({
            "title": "Environment",
            "value": "Test",
            "short": "true"
        })

        actual = logger._SlackLogger__build_payload('Test Message',
                                                    'Test Title',
                                                    'Color Name',
                                                    test_fields)

        expected = {
            "channel": "#dummy_channel",
            "username": "Test User",
            "attachments": [
                {'color': 'Color Name',
                 'text': 'Test Message',
                 "title": "Test Title",
                 'mrkdwn_in': ['text', 'fields', 'title'],
                 "fields": [
                     {
                         "title": "Project",
                         "value": "Test Project",
                         "short": "true"
                     }, {
                         "title": "Environment",
                         "value": "Test",
                         "short": "true"
                     }
                 ],
                 }]
        }

        assert expected == actual

    def test_default_log_level(self):
        logger = SlackLogger(DUMMY_WEB_HOOK)
        assert logger.log_level == 20

    def test_values_in_log_levels(self):
        assert LOG_LEVELS == [10, 20, 30, 40]

    def test_to_set_valid_value_log_level(self):
        logger = SlackLogger(DUMMY_WEB_HOOK)

        for lv in [10, 20, 30, 40]:
            logger.set_log_level(lv)
            assert logger.log_level == lv

    def test_to_set_invalid_value_log_level(self):
        logger = SlackLogger(DUMMY_WEB_HOOK)

        for lv in [0, 50, 99, 'INFO']:
            with pytest.raises(ValueError):
                logger.set_log_level(lv)

        with pytest.raises(TypeError):
            logger.set_log_level()

    def test_log_level_threshold(self):
        logger = SlackLogger(DUMMY_WEB_HOOK)

        actual = logger.debug('TEST')
        assert actual is None

        logger.set_log_level(LogLv.WARN)

        actual = logger.info('TEST')
        assert actual is None

        logger.set_log_level(LogLv.ERROR)

        actual = logger.warn('TEST')
        assert actual is None

    def test_post_to_valid_web_hook(self):
        logger = SlackLogger(VALID_WEB_HOOK)
        logger.set_log_level(LogLv.DEBUG)

        fields = [{
            "title": "Project",
            "value": "Test Project",
            "short": "true"
        }, {
            "title": "Environment",
            "value": "Test",
            "short": "true"
        }
        ]

        response = logger.debug("*Test* Message", "Test Title", fields)
        assert response.status_code == 200

        response = logger.info("Test Message", "Test Title", fields)
        assert response.status_code == 200

        response = logger.warn("Test Message", "Test Title", fields)
        assert response.status_code == 200

        response = logger.error("Test Message", "Test Title", fields)
        assert response.status_code == 200

    def test_post_to_invalid_web_hook(self):
        logger = SlackLogger(DUMMY_WEB_HOOK)

        with pytest.raises(Exception) as exc_info:
            logger.error("Test Message", "Test Title")
        assert 'Failed' in str(exc_info.value)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from slackpy.slackpy import SlackLogger, LOG_LEVELS, LogLv

__author__ = 'takahiro_ikeuchi'


class TestSlackLogger:

    def test_channel_value_error(self):
        with pytest.raises(ValueError):
            SlackLogger('http://dummy_url', 'dummy_channel', 'Test User')

    def test_build_payload_with_all_parameters(self):
        logger = SlackLogger('http://dummy_url', '#dummy_channel', 'Test User')
        actual = logger._SlackLogger__build_payload('Test Message',
                                                    'Test Title',
                                                    'Color Name',
                                                    'Fallback Text',
                                                    '')

        expected = {
            "channel": "#dummy_channel",
            "username": "Test User",
            "attachments":
                {
                    "fields": {
                        "title": "Test Title",
                        "text": "Test Message",
                        "color": "Color Name",
                        "fallback": "Fallback Text",
                    }
                }
        }

        assert expected == actual

    def test_build_payload_without_specifying_optional_parameters(self):
        logger = SlackLogger('http://dummy_url')
        actual = logger._SlackLogger__build_payload('Test Message',
                                                    'Test Title',
                                                    'Color Name',
                                                    'Fallback Text',
                                                    '')

        expected = {
            "channel": None,
            "username": "Logger",
            "attachments":
                {
                    "fields": {
                        "title": "Test Title",
                        "text": "Test Message",
                        "color": "Color Name",
                        "fallback": "Fallback Text",
                    }
                }
        }

        assert expected == actual

    def test_build_payload_with_custom_fields(self):
        logger = SlackLogger('http://dummy_url', '#dummy_channel', 'Test User')

        test_fields = []
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
                                                    'Fallback Text',
                                                    test_fields)

        expected = {
            "channel": "#dummy_channel",
            "username": "Test User",
            "attachments":
                [{
                    "fallback": "Fallback Text",
                    "color": "Color Name",
                    "text": "Test Message",
                    "fields": [{
                        "title": "Project",
                        "value": "Test Project",
                        "short": "true"
                    }, {
                        "title": "Environment",
                        "value": "Test",
                        "short": "true"
                    }]
                }]
        }

        assert expected == actual

    def test_default_log_level(self):
        logger = SlackLogger('http://dummy_url')
        assert logger.log_level == 20

    def test_values_in_LOG_LEVELS(self):
        assert LOG_LEVELS == [10, 20, 30, 40]

    def test_to_set_valid_value_log_level(self):
        logger = SlackLogger('http://dummy_url')

        for lv in [10, 20, 30, 40]:
            logger.set_log_level(lv)
            assert logger.log_level == lv

    def test_to_set_invalid_value_log_level(self):
        logger = SlackLogger('http://dummy_url')

        for lv in [0, 50, 99, 'INFO']:
            with pytest.raises(ValueError):
                logger.set_log_level(lv)

        with pytest.raises(TypeError):
            logger.set_log_level()

    def test_log_level_threshold(self):
        logger = SlackLogger('http://dummy_url')

        actual = logger.debug('TEST')
        assert actual is None

        logger.set_log_level(LogLv.WARN)

        actual = logger.info('TEST')
        assert actual is None

        logger.set_log_level(LogLv.ERROR)

        actual = logger.warn('TEST')
        assert actual is None


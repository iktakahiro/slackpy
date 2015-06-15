__author__ = 'takahiro_ikeuchi'

import pytest
from slackpy.slackpy import SlackLogger


class TestSlackLogger:

    def pytest_funcarg__logger(self):

        return SlackLogger('http://dummy_url', '#dummy_channel', 'Test User')

    def test_channel_value_error(self):

        with pytest.raises(ValueError):
            SlackLogger('http://dummy_url', 'dummy_channel', 'Test User')

    def test_build_payload(self, logger):

        actual = logger._SlackLogger__build_payload('Test Message', 'Test Title', 'Color Name')

        expected = {
            "channel": "#dummy_channel",
            "username": "Test User",
            "attachments":
                {
                    "fields": {
                        "title": "Test Title",
                        "text": "Test Message",
                        "color": "Color Name",
                        "fallback": "Test Title",
                    }
                }
        }

        assert expected == actual

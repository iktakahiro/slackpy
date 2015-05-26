__author__ = 'takahiro_ikeuchi'

from slackpy.slackpy import SlackLogger


class TestSlackLogger:

    def pytest_funcarg__logger(self):

        return SlackLogger('http://dummy_url', '#dummy_channel', 'Test User')

    def test_construct_payload(self, logger):

        actual = logger._SlackLogger__construct_payload('Test Message', 'Test Title', 'Color Name')

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

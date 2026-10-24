import sys
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from slackpy import LOG_LEVELS
from slackpy.commandline import main


@pytest.mark.parametrize(('level', 'method'), [
    (10, 'debug'), (20, 'info'), (30, 'warn'), (40, 'error'),
    (1, 'info'), (2, 'warn'), (3, 'error'),
])
def test_cli_levels(level, method, monkeypatch, capsys):
    client = Mock()
    getattr(client, method).return_value = SimpleNamespace(status_code=200)
    monkeypatch.setattr('slackpy.commandline.SlackLogger', Mock(return_value=client))
    monkeypatch.setenv('SLACK_INCOMING_WEB_HOOK', 'https://example.com/webhook')
    monkeypatch.setattr(sys, 'argv', ['slackpy', '-m', 'hello', '-l', str(level)])

    main()

    getattr(client, method).assert_called_once_with('hello', 'Slack Notification')
    assert capsys.readouterr().out == 'True\n'
    assert LOG_LEVELS == [10, 20, 30, 40]


def test_cli_rejects_invalid_level(monkeypatch):
    monkeypatch.setattr(sys, 'argv', ['slackpy', '-m', 'hello', '-l', '99'])
    with pytest.raises(SystemExit) as exc:
        main()
    assert exc.value.code == 2

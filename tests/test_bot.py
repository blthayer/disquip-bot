"""Test bot.py"""

# Standard library:
import logging
import re
import os

# Third party:
import pytest

# Local:
from disquip import bot


@pytest.fixture(params=['!', '?'])
def bot_helper(audio_collection, request):
    stores = audio_collection.store_names
    aliases = {x: [x[0:3].lower()] for x in stores}

    return bot.BotHelper(
        audio_collection=audio_collection,
        aliases=aliases, cmd_prefix=request.param
    )


@pytest.fixture()
def bot_inst(bot_helper):
    return bot.DisQuipBot(bot_helper=bot_helper)


@pytest.fixture()
def prefix(bot_helper):
    return bot_helper.cmd_prefix


class TestBotHelper:
    """Test the bot helper."""

    def test_logging(self, bot_helper, caplog):
        """Log a message."""
        caplog.set_level(level=logging.INFO)
        bot_helper.log.info('hello!')
        assert "hello!" in caplog.text

    def test_ignore_non_prefixed(self, bot_helper):
        """Parse a message that does not start with the prefix."""
        msg, file = bot_helper.parse_message('howdy, bot!')
        assert msg is None
        assert file is None

    def test_general_help(self, bot_helper, prefix):
        """Check expected results of !help."""
        msg, file = bot_helper.parse_message(f'{prefix}help')

        # No file for help.
        assert file is None

        # The help message should contain all the aliases and all the
        # commands.
        for cmd in bot_helper.audio_collection.store_names:
            assert re.search(fr'\s{prefix}{cmd}\s', msg)

        for alias in bot_helper.alias_map.keys():
            assert re.search(fr'\s{prefix}{alias}\s', msg)

    def test_help_for_alias(self, bot_helper, prefix):
        """Check that we can lookup by alias."""
        alias = list(bot_helper.alias_map.keys())[0]
        # sanity:
        assert alias == 'one'
        # Get help:
        msg, file = bot_helper.parse_message(f'{prefix}help {alias}')
        # No file.
        assert file is None
        # Check on the message.
        efix = re.escape(prefix)
        assert re.search(rf'Available quips for "{efix}{alias}"', msg)
        for key, file in bot_helper.audio_collection.audio_stores[
                bot_helper.alias_map[alias]].file_map.items():
            assert re.search(rf'\s{key}\s', msg)
            assert re.search(rf'\s{os.path.splitext(file)[0]}\s', msg)

    def test_help_for_cmd(self, bot_helper, prefix):
        """Check that we can lookup by command."""
        cmd = bot_helper.audio_collection.store_names[-1]
        msg, file = bot_helper.parse_message(f'{prefix}help {cmd}   ')
        assert file is None
        assert cmd in msg

    def test_nonexistent_cmd(self, bot_helper, prefix):
        msg, file = bot_helper.parse_message(f'{prefix}badcmd 10')
        assert file is None
        assert f'Command "{prefix}badcmd" does not exist.' in msg
        assert f'{prefix}help' in msg

    def test_non_integer(self, bot_helper, prefix):
        msg, file = bot_helper.parse_message(f'{prefix}one eight')
        assert file is None
        assert 'Only integer command arguments are allowed' in msg

    def test_valid(self, bot_helper, prefix):
        msg, file = bot_helper.parse_message(f'{prefix}two 2')
        assert msg is None
        # Hard-coding based on the fixtures for temporary directoreis
        # and files:
        assert 'aoe' in file
        assert 'wav' in file
        assert bot_helper.audio_collection.top_dir in file
        assert 'two' in file
        assert os.path.exists(file)

    def test_invalid_index(self, bot_helper, prefix):
        msg, file = bot_helper.parse_message(f'{prefix}one 1000')
        assert file is None
        assert 'Argument "1000" for command' in msg
        assert 'not valid' in msg


class TestBot:
    """All the mocking required to test this... no thanks."""

    def test_has_helper(self, bot_inst):
        assert hasattr(bot_inst, 'bot_helper')

    def test_has_ffmpeg(self, bot_inst):
        assert hasattr(bot_inst, 'ffmpeg')


"""Helper script to launch the bot."""

# Standard library:
import configparser
import logging
import re
from typing import List

# Local:
from disquip.bot import BotHelper, DisquipBot
from disquip.discover import AudioCollection


def split(str_in: str) -> List[str]:
    """Split string by commas."""
    return [x.strip() for x in re.split(r'\s*,\s*', str_in)]


if __name__ == '__main__':
    # Get configuration.
    config = configparser.ConfigParser()
    config.read('disquip.ini')
    dqc = config['disquip']

    # Get a list of audio extensions.
    audio_extensions = split(dqc['audio_extensions'])

    # Discover available audio.
    audio_collection = AudioCollection(
        top_dir=dqc['audio_directory'],
        audio_store_kw_args={'audio_extensions': audio_extensions}
    )

    # Set up logging.
    logging.basicConfig(
        level=getattr(logging, dqc['log_level'].upper()),
        format="%(asctime)s [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S%z"
    )

    # Get aliases.
    aliases = {key: split(value) for key, value in config['aliases'].items()}

    # Fire up the bot helper.
    bot_helper = BotHelper(audio_collection=audio_collection, aliases=aliases)

    # Instantiate a DisquipBot.
    bot = DisquipBot(bot_helper=bot_helper, ffmpeg=dqc['ffmpeg_path'],
                     cmd_prefix=dqc['cmd_prefix'])

    # Run it! This will connect to Discord.
    bot.run(dqc['api_token'])

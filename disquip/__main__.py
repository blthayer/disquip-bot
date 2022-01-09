"""Helper script to launch the bot."""

# Standard library:
import configparser
import logging
import os
import re
from typing import List

# disquip.
from disquip.bot import BotHelper, DisQuipBot
from disquip.discover import AudioCollection
from disquip.normalize import normalize


def split(str_in: str) -> List[str]:
    """Split string by commas."""
    return [x.strip() for x in re.split(r"\s*,\s*", str_in)]


def main():
    """Parse disquip.ini and fire up the bot!"""
    # Get configuration.
    config = configparser.ConfigParser()
    config.read("disquip.ini")
    dqc = config["disquip"]

    # Configure logging early
    logging.basicConfig(
        level=getattr(logging, dqc["log_level"].upper()),
        format="%(asctime)s [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S%z",
    )

    # Get a list of audio extensions.
    audio_extensions = split(dqc["audio_extensions"])

    # Extract the ffmpeg_path.
    ffmpeg_path = dqc["ffmpeg_path"]

    # Pre-normalize files.
    if int(dqc["pre_normalize"]):
        # Create a sibling audio directory called "normalized."
        audio_directory = dqc["audio_directory"] + "_normalized"
        try:
            os.mkdir(audio_directory)
        except FileExistsError:
            # No big deal if the directory already exists.
            pass

        # Normalize each directory.
        for sub_dir in os.scandir(dqc["audio_directory"]):
            # Skip non-directories.
            if not sub_dir.is_dir():
                continue

            # Normalize all the files in the directory and put them in
            # the new normalized directory.
            normalize(
                in_dir=sub_dir.path,
                out_dir=os.path.join(audio_directory, sub_dir.name),
                extensions=audio_extensions,
                ffmpeg_path=ffmpeg_path,
            )
    else:
        audio_directory = dqc["audio_directory"]

    # Discover available audio.
    audio_collection = AudioCollection(
        top_dir=audio_directory,
        audio_store_kw_args={"audio_extensions": audio_extensions},
    )

    # Get aliases.
    aliases = {key: split(value) for key, value in config["aliases"].items()}

    # Fire up the bot helper.
    bot_helper = BotHelper(
        cmd_prefix=dqc["cmd_prefix"],
        audio_collection=audio_collection,
        aliases=aliases,
        max_search_entries=int(dqc["max_search_entries"]),
    )

    # Instantiate a DisQuipBot.
    bot = DisQuipBot(bot_helper=bot_helper, ffmpeg=ffmpeg_path)

    # Run it! This will connect to Discord.
    bot.run(dqc["api_token"])


if __name__ == "__main__":
    main()

"""The bot!"""

# Standard library:
import logging
import os
import random
import re
from typing import Dict, Optional, Sequence, Tuple, Union

# Third party:
import attr
import discord
from tabulate import tabulate

# Local:
from .discover import AudioCollection

# Listing of help aliases
HELP = ["help", "h"]
# Listing of random aliases. Make sure to keep the full command in
# position 0.
RANDOM = ["random", "rand", "r"]

RANDOM_CMD_OUT_PREFIX = "Playing quip for "


# noinspection PyDataclass,PyArgumentList
@attr.s(
    repr=True,
    auto_detect=False,
    str=True,
    eq=False,
    order=False,
    hash=False,
    init=True,
    slots=True,
    frozen=False,
    auto_attribs=False,
    kw_only=True,
    collect_by_mro=True,
)
class BotHelper:
    """The bot!"""

    audio_collection: AudioCollection = attr.ib()
    """Instantiated AudioCollection."""

    log: logging.Logger = attr.ib(factory=lambda: logging.getLogger(__name__))
    """Logger for the bot."""

    cmd_prefix: str = attr.ib(default="!")
    """Command prefix to use."""

    aliases: Dict[str, Sequence[str]] = attr.ib(factory=dict)
    """Dictionary of command aliases. Keys should be valid audio
    sub-directories."""

    @aliases.validator
    def validate_aliases(self, attribute, aliases):
        """Ensure that each key in aliases maps to a valid AudioStore."""
        for key in aliases.keys():
            if key not in self.audio_collection.audio_stores:
                raise ValueError(
                    f'Directory "{key}" in given aliases does ' "not exist!"
                )

    alias_map: Dict[str, str] = attr.ib(init=False)
    """Dictionary of aliases to commands."""

    def __attrs_post_init__(self):
        """Build out the alias map."""
        self.alias_map = dict()

        for cmd, aliases in self.aliases.items():
            for alias in aliases:
                self.alias_map[alias] = cmd

    def parse_message(
        self, content: str
    ) -> Tuple[Union[str, None], Union[str, None]]:
        """Parse text messages.

        :param content: Message contents as a string.
        :returns: 2-length tuple, both of which are either string or
            None. The first entry corresponds to a text message that
            should be sent back to the channel. The second entry
            corresponds to an audio file path.
        """
        # Only look at commands that start with the prefix.
        if not content.startswith(self.cmd_prefix):
            return None, None

        # Remove leading + trailing space, cast to lower case, split
        # by spaces.
        tokens = content.strip().lower().split(" ", maxsplit=1)

        # Remove the prefix.
        cmd_str = re.sub(re.escape(self.cmd_prefix), "", tokens[0])

        # Help:
        if cmd_str in HELP:
            if len(tokens) == 2:
                return self._create_help(store=tokens[1]), None
            else:
                return self._create_help(store=None), None

        # Disconnect:
        elif cmd_str == "disconnect":
            return "disconnect", None

        # Ignore commands with more than 1 argument.
        if len(tokens) > 2:
            return None, None

        # Handle the special random case.
        if cmd_str in RANDOM:
            if len(tokens) == 1:
                # Full blind random. We need to weight the stores by
                # the number of files they have to ensure all quips
                # have an equal probability.
                store_name = random.choices(
                    list(self.audio_collection.audio_stores.keys()),
                    weights=[
                        x.file_count
                        for x in self.audio_collection.audio_stores.values()
                    ],
                    k=1,
                )[0]

            else:
                # Look up the store. Gross copy + pasting... I sure do
                # hope I don't have to add too many more features! :)
                store_name = self._get_store_name(tokens[1])
                if store_name is None:
                    return self._bad_command(tokens[1]), None

            # Select a random file.
            r_idx = random.randrange(
                1,
                self.audio_collection.audio_stores[store_name].file_count + 1,
            )

            file = self.audio_collection.get_path(
                store_name=store_name, idx=r_idx
            )

            # Return something like 'Playing random quip for "aoe3 2"'
            # along with the file name.
            return (
                (
                    f'{RANDOM_CMD_OUT_PREFIX}"{self.cmd_prefix}{store_name} "'
                    f'{r_idx}"'
                ),
                file,
            )

        # Now we've got a simple command. It's validity is still in
        # question, however.
        cmd = self._get_store_name(cmd_str)
        if cmd is None:
            return self._bad_command(tokens[0]), None

        try:
            idx = int(tokens[1])
        except (ValueError, TypeError):
            return (
                "Only integer command arguments are allowed. You gave "
                f"{tokens[1]}."
            ), None

        try:
            file = self.audio_collection.get_path(store_name=cmd, idx=idx)
        except IndexError:
            return (
                f'Argument "{tokens[1]}" for command "{tokens[0]}" is not '
                f'valid. Type "{self.cmd_prefix}help" for help.'
            ), None
        else:
            return None, file

    def _bad_command(self, cmd: str) -> str:
        return (
            f'Command "{cmd}" does not exist. '
            + f'Type "{self.cmd_prefix}help" to list commands.'
        )

    def _get_store_name(self, cmd: str) -> Union[str, None]:
        """Look up an audio store given a command, which could be an
        alias.

        :param cmd: Either a command or an alias.
        :returns: Valid audio store name or None if one cannot be found.
        """
        # Nothing to do if this is a valid collection name.
        if cmd in self.audio_collection.audio_stores:
            return cmd

        # Look it up in the alias_map. Return None if not found.
        return self.alias_map.get(cmd, None)

    def _create_help(self, store: Optional[str] = None) -> str:
        """Create help message.

        :param store: Either an audio store name or an alias.

        TODO: Currently the help is created dynamically, but it's
            actually static.
        """

        # For convenience, get prefix + help.
        all_help = " or ".join(
            [f'"{self.cmd_prefix}{help_}"' for help_ in HELP]
        )
        help_ = f"{self.cmd_prefix}help"

        # Initialize the message.
        msg = ""

        if store is None:
            # General help.
            msg += (
                f"- Help can be accessed via commands {all_help}.\n"
                f'- The general command syntax is "{self.cmd_prefix}<command> '
                '<number>" where numbers start at 1.\n'
                f"- To get help on a specific command, use "
                f'"{help_} <command>" or "{help_} <alias>".\n'
                f"- Help for specific commands can be filtered like "
                f'"{help_} <command> | <pattern>"\n\t-> "<pattern>" must be '
                f"a valid regular expression (case insensitive).\n\t-> "
                f'Filtering example: "{help_} a1 | gold"\n\n'
                f"Available commands:"
            )

            # Initialize a list. We'll turn it into a table later.
            # Headers will be command, aliases, num commands
            cmd_list = []
            cmd_headers = ["Command", "Alias(es)", "Number of Quips"]

            # Add in the disconnect listing.
            cmd_list.append((f"{self.cmd_prefix}disconnect", "N/A", "N/A"))

            # Add in random listing.
            cmd_list.append(
                (
                    f"{self.cmd_prefix}{RANDOM[0]}",
                    ", ".join(
                        [f"{self.cmd_prefix}{alias}" for alias in RANDOM[1:]]
                    ),
                    "N/A",
                )
            )

            # Loop over the available audio stores.
            for key, audio_store in self.audio_collection.audio_stores.items():

                # First entry will be the key.
                sub_list = [f"{self.cmd_prefix}{key}"]

                # Now, try to find aliases.
                aliases = self.aliases.get(key, False)
                if aliases:
                    # Prefix.
                    prefixed = [
                        f"{self.cmd_prefix}{alias}" for alias in aliases
                    ]
                    # Moosh into a string.
                    sub_list.append(", ".join(prefixed))
                else:
                    # No aliases. Use the empty string.
                    sub_list.append("")

                # Add the number of commands.
                sub_list.append(audio_store.file_count)

                # Tack it onto our command list.
                cmd_list.append(sub_list)

        else:
            # Help for a specific command.

            # Support for help filtering.
            _split = store.split("|", maxsplit=1)
            if len(_split) > 1:
                store = _split[0].strip()
                pattern = _split[1].strip()
            else:
                pattern = None

            # See if the user is asking help for the random command.
            if store in RANDOM:
                cmd = f'"{self.cmd_prefix}{RANDOM[0]}"'
                cmd_example = f'"{self.cmd_prefix}{RANDOM[0]} <command>"'
                msg = (
                    f"The {cmd} command can be used "
                    f"In one of two ways:\n- No arguments (e.g. {cmd}): "
                    "Randomly choose both a command and a quip.\n"
                    f"- Passing a valid command as an argument (e.g. "
                    f"{cmd_example}): Randomly choose a quip for the given "
                    f"command."
                )
                return msg

            elif store == "disconnect":
                cmd = f'"{self.cmd_prefix}disconnect"'
                msg = (
                    f"The {cmd} command disconnects the bot from the voice "
                    "channel of the user that gave the command."
                )
                return msg

            msg, cmd_headers, cmd_list = self._create_help_for_store(store, msg, pattern)

            if (cmd_headers is None) or (cmd_list is None):
                return f'"{store}" is not a valid command or alias!'

        # Time to create a table.
        table = tabulate(cmd_list, headers=cmd_headers, tablefmt="fancy_grid")

        # Format and return.
        return f"{msg}\n{table}"

    def _create_help_for_store(self, store, msg, pattern):
        """returns updated message, command headers, and command list.
        """
        # Look up First, look it up.
        audio_store_name = self._get_store_name(store)

        if audio_store_name is None:
            return msg, None, None

        msg += f'Available quips for "{self.cmd_prefix}{store}"'
        if pattern is not None:
            msg += f' filtered by "{pattern}"'
        msg += ":"

        # Now, we're going to build out a table of available
        # commands and the file names without extensions.
        cmd_list = []
        cmd_headers = ["Quip Number", "Quip Description"]

        audio_store = self.audio_collection.audio_stores[audio_store_name]
        for number, file in audio_store.file_map.items():
            # Extract the command.
            _cmd = os.path.splitext(file)[0]

            # Possibly skip this entry if it doesn't match the
            # filter pattern.
            if (pattern is not None) and (
                    not re.search(pattern, _cmd, re.IGNORECASE)
            ):
                continue

            # Append.
            cmd_list.append([number, _cmd])

        return msg, cmd_headers, cmd_list


class DisQuipBot(discord.Client):
    """The bot!"""

    def __init__(
        self, bot_helper: BotHelper, *args, ffmpeg="ffmpeg", **kwargs
    ):
        """Add bot_helper and ffmpeg attributes, pass remaining args
        and kwargs to super constructor.

        :param bot_helper: Instantiated BotHelper object.
        :param ffmpeg: Name of ffmpeg executable if ffmpeg is on the
            path, otherwise full path to ffmpeg.
        """
        self.bot_helper = bot_helper
        self.ffmpeg = ffmpeg
        super(DisQuipBot, self).__init__(*args, **kwargs)

    async def on_ready(self):
        self.bot_helper.log.info("Logged in as {0.user}".format(self))

    async def on_message(self, message: discord.Message):
        # Don't respond to yourself.
        if message.author == self.user:
            return

        # Parse the message.
        msg, audio_file = self.bot_helper.parse_message(message.content)

        # Check for disconnect flag:
        if (msg == "disconnect") and (audio_file is None):
            await self._disconnect_voice(message)
            return

        # Send in text message if applicable.
        # Do not send in the random command message, that should be
        # sent only immediately before playing the file, because we
        # need to check if the user is in a voice channel before we
        # send in this text message.
        elif msg and not msg.startswith(RANDOM_CMD_OUT_PREFIX):
            await self._send_message(channel=message.channel, msg=msg)

        # Get outta here if there's no audio file.
        if audio_file is None:
            return

        # If we have a valid audio file, this is where the fun begins.
        voice_channel = await self._connect_voice(message)

        if voice_channel is None:
            return

        # Send in the random message, if applicable.
        if msg and msg.startswith(RANDOM_CMD_OUT_PREFIX):
            await self._send_message(channel=message.channel, msg=msg)

        # Transform the audio.
        try:
            # https://github.com/Rapptz/discord.py/blob/master/examples/basic_voice.py
            source = discord.PCMVolumeTransformer(
                discord.FFmpegPCMAudio(
                    source=audio_file, executable=self.ffmpeg
                )
            )
        except Exception as exc:
            await message.channel.send("Something went wrong...")
            self.bot_helper.log.exception("Failed to transform audio.")
            return
        else:
            for voice_client in self.voice_clients:
                # Only quip if we're in the correct channel.
                if voice_client.channel.id != voice_channel.id:
                    continue

                # If the bot is currently playing, stop.
                if voice_client.is_playing():
                    voice_client.stop()

                # Play the new source.
                voice_client.play(source)

        # Th, th, th, th, that's all, folks!
        return

    async def _send_message(self, channel: discord.TextChannel, msg):
        # Content is apparently limited to 2000 characters.
        if len(msg) < 2000:
            await channel.send(self._format_msg(msg))
        else:
            # Chunk it up. Start by dropping the triple back ticks.
            # Break up by newlines.
            lines = msg.split("\n")

            # Initialize the chunk to send.
            chunk = ""
            for line in lines:
                # The 7 comes from triple backticks * 2 plus a
                # newline.
                if len(chunk) + len(line) + 7 < 2000:
                    chunk += line + "\n"
                else:
                    # Send in the chunk, but exclude the last
                    # newline.
                    await channel.send(self._format_chunk(chunk))
                    # Reset the chunk.
                    chunk = line + "\n"

            # Send the last chunk.
            if len(chunk) > 0:
                await channel.send(self._format_chunk(chunk))

    def _format_chunk(self, chunk):
        # Exclude the newline character at the end of the chunk.
        return self._format_msg(chunk[0:-1])

    @staticmethod
    def _format_msg(msg):
        return f"```{msg}```"

    async def _connect_voice(self, message):
        # Get the relevant voice channel.
        voice_channel = self._get_user_voice_channel(message)

        # If they're not in one, chastise them.
        if voice_channel is None:
            await message.channel.send(
                "Hey there troll, you aren't in a voice channel! "
                "No quips for you!"
            )
            return None

        # Attempt to connect.
        try:
            await voice_channel.connect()
        except discord.ClientException as exc:
            if "already connected" in exc.args[0].lower():
                # Already connected, do nothing.
                pass
            else:
                raise exc

        return voice_channel

    @staticmethod
    def _get_user_voice_channel(message):
        # Reference: https://stackoverflow.com/a/53790124/11052174
        # Grab the user who sent the command
        user = message.author
        # Access their voice channel.
        try:
            return user.voice.channel
        except AttributeError:
            return None

    async def _disconnect_voice(self, message):
        # Get the relevant voice channel.
        voice_channel = self._get_user_voice_channel(message)

        # If they're not in one, chastise them.
        if voice_channel is None:
            await self._disconnect_not_allowed(message.channel)
            return

        for voice_client in self.voice_clients:
            # Only disconnect if the user is in the correct channel.
            if voice_client.channel.id == voice_channel.id:
                await voice_client.disconnect()
                return

        # If we're here, the user tried to disconnect from a different
        # channel.
        await self._disconnect_not_allowed(message.channel)

    @staticmethod
    async def _disconnect_not_allowed(channel):
        await channel.send(
            "Hey there, troll, you cannot disconnect the DisQuip Bot without "
            "being in the same voice channel as the bot."
        )

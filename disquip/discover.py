"""Helper for discovering audio files."""

# Standard library:
import logging
import os
from typing import Any, Dict, List, Sequence, Union

# Third party:
import attr


# module-level logger, named differently so there's no confusion between which
# logger is being used.
module_log = logging.getLogger(__name__)


def _create_store_logger(store) -> logging.Logger:
    """Creates a :class:`logging.Logger` for a specific :class:`.AudioStore`.

    The name for the logger is based on the store's audio directory
    name: ``disquip.discover.AudioStore.{audio_dir}``. If ``audio_dir``
    includes subdirectories, they are separated by dots (so
    ``foo/bar/baz`` would become ``foo.bar.baz``). ``AudioStore`` will
    also reflect the name of the class, so if a subclass is used at
    some point in time, the name of the logger will reflect that.

    :param store: The audio store to create a logger for.
    :type store: AudioStore
    """
    # Replace any existing dots in directory names with underscores, and then
    # separate directories with dots.
    no_dots_path = store.audio_dir.replace(".", "_")
    # Separate directories with dots
    dotted_path = ".".join(os.path.split(no_dots_path))
    # Remove any leading dots
    if dotted_path[0] == ".":
        dotted_path = dotted_path[1:]
    # Further normalization is *not* being done, as paths con contain almost
    # anything besides null bytes and '/'
    logger_name = f"{__name__}.{store.__class__.__name__}.{dotted_path}"
    module_log.debug(
        "Mapping AudioStore.audio_dir (%s) to logger name '%s'",
        store.audio_dir,
        logger_name
    )
    return logging.getLogger(logger_name)


@attr.s(kw_only=True, slots=True)
class AudioStore:
    """Helper class for finding audio files. You could also use this
    to discover other types of files.
    """

    top_dir: str = attr.ib()
    """Top level directory. Full file system path."""

    audio_dir: str = attr.ib()
    """Name of audio directory relative to ``top_dir``."""

    audio_extensions: Sequence[str] = attr.ib(default=('mp3', 'wav'))
    """Audio extensions to look for. No periods, please."""

    log: logging.Logger = attr.ib(
        default=attr.Factory(_create_store_logger, takes_self=True),
    )
    """Logger for this AudioStore."""

    # TODO: I think it would be more in-line with the attrs philosophy
    #   to use a Factory rather than the post init hook, but that gets
    #   a bit messy.
    file_map: Dict[int, str] = attr.ib(init=False, repr=False)
    """Mapping of integers to filenames within the ``audio_dir``."""

    def __attrs_post_init__(self):
        """Build the file_map."""

        # List files.
        files = [x for x in os.listdir(self._audio_dir_full)
                 if os.path.splitext(x)[1].replace('.', '')
                 in self.audio_extensions]

        # Sort.
        files.sort()

        # Map integers to files, starting at 1.
        self.file_map = {i + 1: x for i, x in enumerate(files)}

    @property
    def file_count(self) -> int:
        """Number of audio files for the store."""
        return len(self.file_map)

    @property
    def _audio_dir_full(self):
        """Private getter method for full path to directory with the
        audio files.
        """
        return os.path.join(self.top_dir, self.audio_dir)

    def get_path(self, i: int) -> Union[str, None]:
        """Get a file path from an integer string. Returns None if the
        given integer is not a valid mapping.
        """
        # Get file name from integer, defaulting to None.
        file_name = self.file_map.get(i, None)

        # If we have a file, return a full path.
        if file_name is not None:
            return os.path.join(self._audio_dir_full, file_name)

        # We don't have a file. Return None to indicate.
        return None


@attr.s(slots=True, kw_only=True)
class AudioCollection:
    """Collection of AudioStores."""

    top_dir: str = attr.ib()
    """Full path to top-level directory whose subdirectories contain
    audio files.
    """

    audio_store_kw_args: Dict[str, Any] = attr.ib(factory=dict)
    """Keyword arguments to pass to the AudioStores when initializing."""

    audio_stores: Dict[str, AudioStore] = attr.ib(
        init=False,
        default=attr.Factory(
            lambda self: {audio_dir: AudioStore(top_dir=self.top_dir,
                                                audio_dir=audio_dir,
                                                **self.audio_store_kw_args)
                          for audio_dir in os.listdir(self.top_dir)},
            takes_self=True
        ))
    """Dictionary mapping of AudioStores for each subdirectory in
    top_dir.
    """

    def get_path(self, store_name: str, idx: int) -> str:
        """Get a file path from an AudioStore by index.

        :param store_name: Name of a subdirectory. Must be a key in
            self.audio_stores.
        :param idx: Integer index to look up.
        :raises ValueError, IndexError: ValueError if the store_name
            is not valid, IndexError if the idx is not valid.
        """

        # Look up the AudioStore.
        try:
            audio_store = self.audio_stores[store_name]
        except KeyError:
            raise ValueError(f'No such audio_name, {store_name}.') from None

        # Lookup the path from the AudioStore given the index.
        path = audio_store.get_path(idx)

        # Raise exception if the index is not present.
        if path is None:
            raise IndexError(f'No such integer key, {idx}')

        # All done!
        return path

    @property
    def store_names(self) -> List[str]:
        """Return the names of the available stores."""
        keys = list(self.audio_stores.keys())
        keys.sort()
        return keys

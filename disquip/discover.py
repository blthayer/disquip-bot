"""Helper for discovering audio files."""

# Standard library:
import os
from typing import Sequence, Union

# Third party:
import attr


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

    # TODO: I think it would be more in-line with the attrs philosophy
    #   to use a Factory rather than the post init hook, but that gets
    #   a bit messy.
    file_map: dict = attr.ib(init=False, repr=False)
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

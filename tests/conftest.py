"""Pytest fixtures."""

# Standard library:
import tempfile as tf

# Third party:
import pytest


@pytest.fixture()
def temp_dir_top():
    """Create a temporary directory for building out a file structure
    of sub directories and audio files.
    """
    with tf.TemporaryDirectory() as dir_name:
        yield dir_name


@pytest.fixture()
def temp_pre_suf_one():
    """Prefixes and suffixes for temporary files."""
    return [('a file', 'mp3'), ('003 taunt', 'wav'), ('help', 'txt')]


@pytest.fixture()
def temp_pre_suf_two():
    """A few more extensions."""
    return [('25', 'mp3'), ('aoe', 'wav'), ('README', 'txt'),
            ('error', 'wav8'), ('audio', 'mp3'), ('data', 'csv')]


@pytest.fixture()
def temp_filesystem(temp_dir_top, temp_pre_suf_one, temp_pre_suf_two):
    """Create a simple little temporary file system."""
    # Since we're using the temp_dir_top inside a context manager, no
    # need to use them here --> it'll clean everything up on exit.
    # Start by creating a pair of temporary directories.
    td_1 = tf.TemporaryDirectory(dir=temp_dir_top, prefix='one')
    td_2 = tf.TemporaryDirectory(dir=temp_dir_top, prefix='two')

    # Make temporary files in the temporary directories.
    for prefix, suffix in temp_pre_suf_one:
        tf.NamedTemporaryFile(prefix=prefix, suffix=('.' + suffix),
                              dir=td_1.name, delete=False)

    for prefix, suffix in temp_pre_suf_two:
        tf.NamedTemporaryFile(prefix=prefix, suffix=('.' + suffix),
                              dir=td_2.name, delete=False)

    # Return the name of the top-level directory.
    yield temp_dir_top

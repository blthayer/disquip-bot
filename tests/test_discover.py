"""Test discover.py"""

# Standard library:
import os
import typing

# Third party:
import pytest

# Local:
from disquip import discover


def test_file_structure(temp_filesystem, temp_pre_suf_one, temp_pre_suf_two):
    """Meta test for the temporary filesystem that gets created by the
    fixtures.
    """
    # Ensure the directory can be found.
    assert os.path.exists(temp_filesystem)

    # Now, there should be two sub-directories.
    sub = os.listdir(temp_filesystem)
    assert len(sub) == 2

    # Get paths to the sub directories.
    sub_one = os.path.join(temp_filesystem, sub[0])
    sub_two = os.path.join(temp_filesystem, sub[1])

    # They should exist.
    assert os.path.exists(sub_one)
    assert os.path.exists(sub_two)

    # They should contain files.
    assert len(os.listdir(sub_one)) == len(temp_pre_suf_one)
    assert len(os.listdir(sub_two)) == len(temp_pre_suf_two)


@pytest.fixture(params=[0, 1])
def audio_store_and_expected_files(temp_filesystem, request) \
        -> typing.Tuple[discover.AudioStore, int]:
    """Return an AudioStore along with the number of files it should
    have.
    """
    audio_dir = os.listdir(temp_filesystem)[request.param]
    if audio_dir.startswith('one'):
        expected_files = 2
    elif audio_dir.startswith('two'):
        expected_files = 3
    else:
        raise ValueError(f'Did not expect audio_dir {audio_dir}.')

    audio_store = discover.AudioStore(
        top_dir=temp_filesystem, audio_dir=audio_dir)
    return audio_store, expected_files


class TestAudioStore:
    """Test the AudioStore class."""

    def test_map(self, audio_store_and_expected_files):
        """Ensure the file map is as expected.
        """
        audio_store = audio_store_and_expected_files[0]
        expected_files = audio_store_and_expected_files[1]

        # Check number of files.
        assert len(audio_store.file_map) == expected_files

        # Ensure the keys are as expected.
        key_list = list(audio_store.file_map.keys())
        assert key_list == [x + 1 for x in range(len(key_list))]

        # Ensure the values are as expected.
        for key, file in audio_store.file_map.items():

            # Check the extension.
            ext = os.path.splitext(file)[1].replace('.', '')
            assert ext in audio_store.audio_extensions

            # File should exist.
            assert os.path.exists(
                os.path.join(
                    audio_store.top_dir, audio_store.audio_dir, file))

    def test_file_count(self, audio_store_and_expected_files):
        """Check the file_count property."""
        audio_store = audio_store_and_expected_files[0]
        expected_files = audio_store_and_expected_files[1]

        # Check number of files.
        assert audio_store.file_count == expected_files

    def test_get_path(self, audio_store_and_expected_files):
        """Check the get_path method."""
        audio_store = audio_store_and_expected_files[0]
        expected_files = audio_store_and_expected_files[1]

        for i in range(expected_files):
            assert os.path.exists(audio_store.get_path(i+1))

    @pytest.mark.parametrize('key', (10293834, '1', 'my_file'))
    def test_get_path_returns_none_for_bad_key(
            self, audio_store_and_expected_files, key):
        """Expect None return for nonexistent key."""
        audio_store = audio_store_and_expected_files[0]
        assert audio_store.get_path(key) is None

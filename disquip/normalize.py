"""Normalize audio files using ffmpeg-normalize:
https://github.com/slhck/ffmpeg-normalize
"""

import logging
import os
import subprocess


log = logging.getLogger(__name__)


def normalize(in_dir, out_dir, extensions, ffmpeg_path=None):
    # If given an ffmpeg path, use it.
    if ffmpeg_path is not None:
        env = os.environ.copy()
        env['FFMPEG_PATH'] = ffmpeg_path
    else:
        env = None

    # Get a listing of files in the directory.
    files = [os.path.join(in_dir, x) for x in os.listdir(in_dir)
             if os.path.splitext(x)[1].replace('.', '') in extensions]
    if files:
        log.debug("Normalizing files: %s", files)
        # Due to issues with short files we have to use simple peak
        # normalization rather than the better default of EBU R128.
        # https://github.com/slhck/ffmpeg-normalize/issues/87
        subprocess.run(
            ['ffmpeg-normalize'] + files
            + ['-of', out_dir, '-nt', 'peak', '-t', '0', '-c:a', 'libmp3lame',
            '-ext', 'mp3'],
            env=env)
    else:
        log.error("No audio files found in '%s'", in_dir)

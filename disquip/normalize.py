"""Normalize audio files using ffmpeg-normalize:
https://github.com/slhck/ffmpeg-normalize
"""

import logging
import os
import re
import subprocess

log = logging.getLogger(__name__)


def _log_ffmpeg_normalize(msg, level):
    """Helper to pass messages from ffmpeg-normalize to our logger."""
    method = getattr(log, level)
    method(f"[ffmpeg-normalize]: %s", msg)


def _fix_ffmpeg_normalize_output(output):
    """Especially on Linux, we're getting some weird byte style (I
    think, I don't dabble in that low level stuff) characters showing up
    in the output from ffmpeg-normalize. Fix that."""
    return re.sub(r"\x1b\[.{1,4}m", "", output)


def normalize(in_dir, out_dir, extensions, ffmpeg_path=None):
    # If given an ffmpeg path, use it.
    if ffmpeg_path is not None:
        env = os.environ.copy()
        env["FFMPEG_PATH"] = ffmpeg_path
    else:
        env = None

    # Get a listing of files in the directory.
    files = [
        os.path.join(in_dir, x)
        for x in os.listdir(in_dir)
        if os.path.splitext(x)[1].replace(".", "") in extensions
    ]
    if files:
        log.debug("Normalizing files: %s", files)
        # Due to issues with short files we have to use simple peak
        # normalization rather than the better default of EBU R128.
        # https://github.com/slhck/ffmpeg-normalize/issues/87
        #
        # ffmpeg-normalize logs an error for each file that already
        # exists. For our use-case, this is quite annoying. So, we'll
        # capture the output and filter those messages.
        result = subprocess.run(
            ["ffmpeg-normalize"]
            + files
            + [
                "-of",
                out_dir,
                "-nt",
                "peak",
                "-t",
                "0",
                "-c:a",
                "libmp3lame",
                "-ext",
                "mp3",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
        )

        # Split stdout and stderr by newlines after stripping off odd
        # byte style output that shows up.
        stdout = re.split(
            r"\r*\n",
            _fix_ffmpeg_normalize_output(result.stdout.decode("utf-8")),
        )
        stderr = re.split(
            r"\r*\n",
            _fix_ffmpeg_normalize_output(result.stderr.decode("utf-8")),
        )

        # Loop and log.
        # TODO: It would probably be better to directly pipe this from
        #   the subprocess to a log so the logging occurs in real time.
        #   Oh well, not worth the effort at this point :)
        for out in stdout:
            # Skip empty lines
            if len(out) == 0:
                continue

            # Ignore "nuisance" logging.
            elif re.match(
                r"ERROR: Output file .+ already exists, skipping.", out
            ):
                continue

            # Log other errors to the error level.
            elif out.startswith("ERROR"):
                _log_ffmpeg_normalize(msg=out, level="error")

            # Log anything else we find to info.
            # TODO: We could certainly be more sophisticated here and
            #   detect the log level.
            else:
                _log_ffmpeg_normalize(msg=out, level="info")

        # Log all stderr.
        log.debug("")
        for out in stderr:
            if len(out) > 0:
                _log_ffmpeg_normalize(msg=out, level="error")

    else:
        log.error("No audio files found in '%s'", in_dir)

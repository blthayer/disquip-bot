disquip-bot
===========

An easy-to-use Discord soundboard bot. BYO audio files and quip away!

Introduction
------------

The purpose of the DisQuip Bot project is to provide a simple
sound board bot that is easy to install, configure, and run. After
installation, simply create a directory structure with your own quips
(audio files) and run the bot! Then, head on over to your favorite
Discord server, and punch in commands like ``!aoe3 11`` and the bot
will play the corresponding quip for you into your voice channel.

Head on over to `Contents`_ to get started.

Backstory
^^^^^^^^^

I found myself wishing I could easily play taunts from the
`Age of Empires`_ video games while playing other games with my friends.
So, I built out a prototype that went by the name of "AOE Taunt Board."
It was a hit, so I figured I'd make a publicly distributable version for
you, the reader!

Contents
--------

1.  `Introduction`_

    a.  `Backstory`_

2.  `Installation`_

    a.  `Preliminaries`_
    b.  `Prerequisites`_
    c.  `Install FFmpeg and Other Prerequisite Packages`_
    d.  `Configure Python Virtual Environment and Install DisQuip Bot`_

3.  `Audio Files`_

    a.  `Where Can I Find Audio Files?`_

4.  `Discord Configuration`_

    a.  `Create a Discord Application`_
    b.  `Add the Bot to Servers`_

5.  `Configuration`_

    a.  `API Token`_
    b.  `Aliases`_

6.  `Run the Bot`_

7. `Using the Bot`_

    a.  `Help`_

8. `Hosting the DisQuip Bot On a Server`_
9. `Changelog`_


Installation
------------

Depending on your personal level of computer literacy, installation
takes ~10-60 minutes.

Preliminaries
^^^^^^^^^^^^^
Please follow the directions below before moving forward.

1.  Create a new directory called ``disquip-bot`` in your home directory.
    On Windows, that's typically ``C:\Users\<youruser>\disquip-bot``.
    To keep these directions simple, this directory will be referred to as
    ``~/disquip-bot`` going forward.

2.  Download `disquip.ini`_ and place it in ``~/disquip-bot``. Later, in
    `Configuration`_ we'll be modifying this file.

3.  Create a new directory called ``audio_files`` underneath
    ``~/disquip-bot``. This is where we'll be placing our quips later on
    (`Audio Files`_).

Prerequisites
^^^^^^^^^^^^^

TL;DR:

-   `Python`_ >= 3.6
-   `FFmpeg`_
-   (For Linux, Mac should be similar): ``libff-dev``, ``libnacl-dev``, ``python-dev``
-   (For Windows only): `7zip`_
-   (For Windows only, **OPTIONAL**): `Notepad++`_

DisQuip Bot *should* be operating system agnostic, but to date has only
been tested on Windows (I know, gross.) and Linux (specifically, on a
Debian-like distribution).

DisQuip Bot is a Python program and thus requires that you install
`Python`_. Specifically, ensure you are running a version of Python
>= 3.6. Before going any further take a moment to `download Python`_ and
then install it.

For Windows users: later we'll be downloaded a compressed ``.7z``
archive that we'll need to extract. For extraction, we'll use `7zip`_.
Please download and install.

Install FFmpeg and Other Prerequisite Packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Refer to the `FFmpeg`_ website and/or `discord.py`_'s
`installation instructions <https://discordpy.readthedocs.io/en/latest/intro.html#installing>`__
if the directions here are inadequate.

**Mac**

Sorry, I don't have a Mac. Feel free to send me a pull request with
Mac directions!

**Linux (Debian)**

::

    apt-get update
    apt-get install ffmpeg libffi-dev libnacl-dev python3-dev

**Windows**

Fortunately, helpful folks like Gyan Doshi exist and provide pre-built
FFmpeg distributions. Installing is as simple as:

1.  Download the appropriate build from
    `gyan.dev`_. I've successfully used the
    `git-essentials FFmpeg build`_. You can find other builds at
    `FFmpeg`_ or build it yourself from source code.
2.  Extract the downloaded ``.7z`` archive to ``~/disquip-bot/ffmpeg``
    using `7zip`_. For me, that looks like:

    a.  Navigate to the ``Downloads`` folder (Typically
        ``C:\Users\<your user>\Downloads``
    b.  Right click the downloaded ``.7z`` file (it'll be named
        like ``ffmpeg-2020-10-11-git-7ea4bcff7b-essentials_build.7z``)
    c.  Hover over ``7-zip``, and selecting ``Extract files...``.
    d.  In the pop-up:

        -   Change ``Extract to:`` entry to ``~/disquip-bot/ffmpeg``,
            replacing ``~`` with your full file system path.
        -   Uncheck the checkbox directly below the ``Extract to`` box.
        -   Check the ``Eliminate duplication of root folder`` box.
        -   Click ``OK``.

After following the directions above, you should have one sub-folder in
``~/disquip-bot/ffmpeg`` named something like
``ffmpeg-2020-10-11-git-7ea4bcff7b-essentials_build``. Within that
sub-folder should be directories called ``bin``, ``doc``, and
``presets``. There will also be a pair of files called ``LICENSE`` and
``README``.

Later on in `Configuration`_, you'll need the full file system path to
``ffmpeg.exe`` in the ``bin`` directory.

Configure Python Virtual Environment and Install DisQuip Bot
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After you've installed Python, we'll be configuring what's known as a
virtual environment to install Python dependencies as well as the
DisQuip Bot. Here are directions for Windows (similar on Mac/Linux):

1.  Start a Command Prompt (shortcut: ``Win + R`` keys, type ``cmd``,
    hit ``Enter`` key).
2.  Change directories to your ``~/disquip-bot`` directory using the
    ``cd`` command. This should work: ``cd %USERPROFILE%\disquip-bot``.
3.  Run the command ``py -3 -m venv venv`` to create a virtual
    environment directory called ``venv`` in ``~/disquip-bot``. If you
    have multiple versions of Python 3.x installed, you can specify
    ``py -3.8``, for example.
4.  Activate the virtual environment by running the command
    ``venv\Scripts\activate.bat``. Your command line should now be
    prefixed with "(venv)".
5.  Python installs packages with a tool called ``pip``. Update it by
    running: ``python -m pip install --upgrade pip``.
6.  Install the DisQuip Bot and its dependencies by running
    ``python -m pip install disquip-bot``.

Audio Files
-----------

As mentioned in the second sentence of this document, this project is a
"bring your own audio files" project. If you've followed the directions,
you should have a directory called ``audio_files`` in your
``~/disquip-bot`` directory. Within that ``audio_files`` directory
there must be subdirectories that contain audio files. An example
structure might look like::

    -- audio_files:
    ------ AgeOfEmpires1
    ---------- 01 Yes.mp3
    ---------- 02 No.mp3
    ------ MontyPython
    ---------- I fart in your general direction.wav
    ---------- Bleed on me.wav
    ---------- Weirdo.wav

How this structure is set up has meaning. To explain via example,
assuming commands are prefixed with an exclamation mark (``!``):

There will be two available commands, ``!AgeOfEmpires1`` and
``!MontyPython`` (case insensitive). You can define `Aliases`_ for
shorter names. The ``!AgeOfEmpires1`` command can accept 1 of 2 possible
arguments, "1," or "2". A quip command would look like
``!AgeOfEmpires1 2``, which would stream "02 No.mp3" into your current
voice channel.

Similarly, the ``!MontyPython`` command can accept 1 of 3 arguments,
"1," "2," or "3." The files are sorted alphanumerically, so
``!MontyPython 1`` would stream ``Bleed on me.wav`` into your
current audio channel.

It's worth noting that the names of the audio files, excluding their
file extensions (*e.g.*, ``.mp3``), will be used in creating `Help`_
messages. So, the more descriptive, the better!

Where Can I Find Audio Files?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The internet is full of audio files that are available to you for no
cost. For example, `myinstants.com`_ has all sorts of files. You can
also easily make your own using your PC's microphone. Also, `FFmpeg`_
is a *very* powerful tool that you could use to create clips. Want
nearly 1,000 community-sourced quips from 1998? Head on over to
`Age of Empires Heaven`_.

If you love `Age Of Empires`_ here are a few suggestions:

-   **Age of Empires 2 on Steam**: I found the taunts in
    ``C:\Program Files (x86)\Steam\steamapps\common\Age2HD\resources\en\sound\taunt``.
-   **Age of Empires 3 on Steam**: I found the taunts in
    ``C:\Program Files (x86)\Steam\steamapps\common\Age Of Empires 3\bin\Sound\taunts``
-   **Age of Empires 1**: A tad more work, and the gain is rather
    minimal. If you're dedicated, read on:

    -   Subscribe to the "Age of Empires 1 Taunt Pack" on the
        `Steam Workshop <https://steamcommunity.com/sharedfiles/filedetails/?id=137168612>`__.
    -   The mod will download automatically in Steam.
    -   Check the logs at
        ``C:\Program Files (x86)\Steam\steamapps\common\Age2HD\Logs\2020.10.03-0839.59``
        (the ultimate file name will of course be different).
    -   You should find a ``Mod`` text file. Open it up.
    -   Find where the mod was installed. For me it was at
        ``C:\Program Files (x86)\Steam\steamapps\workshop\content\221380\927865693``.
    -   Go there, and dig in:
        ``C:\Program Files (x86)\Steam\steamapps\workshop\content\221380\137168612\resources\en\sound\taunt``.
    -   Copy the taunt files to your Age of Empires directory. Perhaps
        ``aoe1`` to keep it short?

Discord Configuration
---------------------

It took me more time than I had hoped to figure this out, so hopefully
these directions save you some time. We need to
`Create a Discord Application`_ and then `Add the Bot to Servers`_.

Create a Discord Application
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1.  For starters, you of course need to have a `Discord`_ account.
2.  Navigate to the `Discord applications`_ site.
3.  Click on ``New Application``
4.  **OPTIONAL**: If you'd like, add a custom icon in the ``APP ICON``
    area. Perhaps a snip-and-sketch of your favorite game?
5.  Click on the ``Bot`` tab in the left-hand ``SETTINGS`` area.
6.  Click the ``Add Bot`` button.
7.  In the pop-up window, click on ``Yes, do it!``.

Don't close that web browser or tab! Stay right where you are and move
on to `Add the Bot to Servers`_.

Add the Bot to Servers
^^^^^^^^^^^^^^^^^^^^^^

Scroll down to the bottom of the ``OAuth2`` tab for the application you
made in `Create a Discord Application`_. In the ``SCOPES`` area check
the ``bot`` box.

The DisQuip bot only needs the following permissions:
-   **TEXT PERMISSIONS**: "Send Messages"
-   **VOICE PERMISSIONS**: "Connect" and "Speak"

Scroll down to the ``BOT PERMISSIONS`` area and click the appropriate
boxes corresponding the permissions listed above.

Finally, click on the ``Copy`` button in the ``SCOPES`` area. Paste
the link into a new tab in your web browser. You'll need to login to
Discord. A pop-up will appear and you'll need to select a server from
the ``ADD BOT TO:`` drop-down and then click ``Continue``. Click
``Authorize`` and then prove you aren't a robot yourself.

If you've followed all the steps in this section, your bot now should
have permissions to listen to and send text messages as well as send
audio messages into a voice channel.

Don't close your web browser just yet! Keep that tab open and continue
to `Configuration`_.

Configuration
-------------

All the necessary configuration parameters for DisQuip Bot are defined
in ``disquip.ini``, which you should have downloaded during the
`Preliminaries`_. Rather than list every configuration
option here, they're all listed in ``disquip.ini``. Open that file with
your favorite text editor (I strongly recommend `Notepad++`_ if you're
using Windows so that you can get syntax highlighting) and update the
file according to your installation. Please read the entire file. Don't
forget to hit "save" when you're done! :)

Here are a couple areas worth discussion explicitly:

API Token
^^^^^^^^^

Remember when I asked you to keep your tab open from the `Discord applications`_
site? Here's where you'll use it. In the ``Bot`` tab, find the are where
it says ``TOKEN``. Click the ``Copy`` button to copy your token to the
clipboard. Use the copied value to update the ``api_token`` field in
``disquip.ini``. Don't forget to save the file.

Aliases
^^^^^^^

It's nice to have descriptive directory names like "monty_python" or
"AgeOfEmpires1" but that can be cumbersome to type for a quick quip.
To alleviate this, the DisQuip Bot supports aliases for commands. Check
out the ``[aliases]`` section of ``disquip.ini``

Run the Bot
-----------

After you've performed all the installation and configuration steps
above, you're ready to run!

1.  Using a command prompt, change directories to ``~/disquip-bot``:
    ``cd %USERPROFILE%\disquip-bot`` (Windows); ``cd ~/disquip-bot``
    (Mac/Linux).
2.  Activate your virtual environment:
    ``venv\Scripts\activate.bat`` (Windows); ``source venv/bin/activate``
    (Mac/Linux).
3.  Execute the command ``disquip-bot`` to fire it up.

When you're done, simply kill the command window you have running or
use ``Ctrl + C`` to stop the program.

Updating Configurations or Audio Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The DisQuip bot does not dynamically detect changes to audio files or
configurations. After making a change, simply stop the bot and start it
again to pick up any changes.

Using the Bot
-------------

The bot will listen to all the text channels of the server(s) you added
it to and look for messages that start with the ``cmd_prefix`` defined
in ``disquip.ini``. This defaults to the exclamation mark (``!``).

The DisQuip Bot will automagically join the voice channel you're
currently in once it receives a valid command. Note that DisQuip Bot can
only be in one voice channel per server at any given time.

Start exploring!

Help
^^^^

Assuming your command prefix is ``!``, simply type ``!help`` into a
text channel the bot has access to. It'll respond with a listing of
available commands and some other helpful information.

Hosting the DisQuip Bot On a Server
-----------------------------------

Rather than running the DisQuip Bot on the same machine you're using to
chat and play games, you may want to host it on a server. This will
preserve resources on your local machine and allow the DisQuip Bot to
stay online even when you aren't.

The ``service`` directory in this repository has one sample
implementation for running the DisQuip Bot as a service on a
`Raspberry Pi 3 Model B`_ running the Raspbian GNU/Linux 9 (stretch)
operating system. The directions there should apply to many different
flavors of Linux. If you'd like to get started, check out
``service/README.rst``.

Changelog
---------

1.1.8
^^^^^

Add new "lucky" command. Like "search," but plays the first found quip
into the audio channel.

1.1.7
^^^^^

-   Fix bug in search limiting. D'Oh!
-   Ensure backwards compatibility. D'Oh!
-   See notes for ``1.1.6``

1.1.6
^^^^^

-   **Please use 1.1.7!**
-   Add configurable maximum number of results for search (introduced in
    ``1.1.5``), defaults to 20.
-   Drop all support for Docker. You can find directions related to
    Docker by viewing this repository at `v1.1.4`_. If you can live
    without the search introduced in ``1.1.5``, you can still pull the
    image for ``1.1.4``::

        docker pull blthayer/disquip-bot:v1.1.4

1.1.5
^^^^^

Adding two methods to filter help:

-   **Please use 1.1.7!**
-   A global ``search`` command (alias: ``s``)
-   Adding the ability to filter help for a given command like ``!help a1 | pattern``

1.1.4
^^^^^

Addressed minor issue with random command when the caller was not in a
voice channel.

1.1.3
^^^^^

Fixes a compatibility issue with Python 3.6 that was introduced in
``v1.1.2``.

1.1.2
^^^^^

- New "disconnect" command: https://github.com/blthayer/disquip-bot/issues/13
- Removed nuisance logging if normalized files already existed: https://github.com/blthayer/disquip-bot/issues/16
- Adding automated Docker image builds: https://github.com/blthayer/disquip-bot/issues/14
- Adding cron job example to service: https://github.com/blthayer/disquip-bot/issues/17

1.1.1
^^^^^

Thanks to `Will Ross`_ for this one. Major logging improvements
throughout the DisQuip Bot.

1.1.0
^^^^^

-   **Backwards incompatible change**: ``disquip.ini`` now requires a
    ``pre_normalize`` field in the ``[disquip]`` section.
-   By default, all audio files will first be pre-normalized to a peak
    amplitude of 0 dB. This is accomplished using `ffmpeg-normalize`_.
-   New ``random`` command!.


.. _7zip: https://www.7-zip.org/
.. _Age of Empires: https://www.ageofempires.com/
.. _Age of Empires Heaven: http://aoe.heavengames.com/downsnew/dwntaunts.shtml
.. _Discord: https://discord.com/
.. _discord.py: https://discordpy.readthedocs.io/en/latest/index.html
.. _Discord applications: https://discord.com/developers/applications
.. _disquip.ini: https://github.com/blthayer/disquip-bot/blob/main/disquip.ini
.. _DisQuip Bot: https://github.com/blthayer/disquip-bot
.. _DisQuip Bot .zip archive: https://github.com/blthayer/disquip-bot/archive/main.zip
.. _DisQuip Bot via git clone: https://github.com/blthayer/disquip-bot.git
.. _Download Python: https://www.python.org/downloads/
.. _FFmpeg: https://ffmpeg.org/
.. _ffmpeg-normalize: https://github.com/slhck/ffmpeg-normalize
.. _git-essentials FFmpeg build: https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z
.. _gyan.dev: https://www.gyan.dev/ffmpeg/builds/
.. _Install Windows Subsystem for Linux: https://docs.microsoft.com/en-us/windows/wsl/install-win10
.. _myinstants.com: https://www.myinstants.com
.. _Notepad++: https://notepad-plus-plus.org/
.. _Python: https://www.python.org/
.. _Raspberry Pi 3 Model B: https://www.raspberrypi.org/products/raspberry-pi-3-model-b/
.. _Will Ross: https://github.com/paxswill
.. _v1.1.4: https://github.com/blthayer/disquip-bot/tree/v1.1.4
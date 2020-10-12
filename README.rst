disquip-bot
===========

An easy-to-use Discord soundboard bot. BYO audio files and quip away!

Introduction
------------

The purpose of the Disquip Bot project is to provide a simple
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

`disquip-bot`_

    `Introduction`_

        `Backstory`_

    `Installation Overview`_
    `Installation Preliminaries`_

        `Download disquip.ini`_
        `Create "audio_files" Directory`_

    `Docker Based Installation`_

        `Install Docker On Windows`_
        `Download the Disquip Bot Docker Image`_

    `Local Installation`_

        `Prerequisites`_
        `Install FFmpeg (Windows)`_
        `Configure Python Virtual Environment and Install Disquip Bot`_

    `Audio Files`_

        `Where Can I Find Audio Files?`_

    `Discord Configuration`_

        `Create a Discord Application`_
        `Add the Bot to Servers`_

    `Configuration`_

        `API Token`_
        `Aliases`_

    `Run the Bot`_

        `Running for Docker Install`_
        `Running for Local Install`_
        `Updating Configurations or Audio Files`_

    `Using the Bot`_

        `Help`_


Installation Overview
---------------------

Depending on your personal level of computer literacy, installation
takes ~10-60 minutes. There are two different ways to install the
Disquip Bot:

-   `Docker Based Installation`_: If you already have Docker installed,
    this is the easiest path to take. If you do not already have Docker,
    note that Docker is a large program (the installer for Docker alone
    was 407MB on 2020-10-11), and it takes a little extra work to
    `Install Docker on Windows`_ compared to to Mac/Linux. However,
    once Docker is installed, there are significantly less steps
    required to get the Disquip Bot running compared to the
    `Local Installation`_.
-   `Local Installation`_: The local installation process is relatively
    straight forward and will lead to a leaner installation if you do
    not have Docker installed and don't plan to install it in the
    future. However, it involves downloading and installing several
    programs as well as manually placing program files in directories of
    your choosing.

Whichever route you choose, be sure to first take care of the
`Installation Preliminaries`_.

Installation Preliminaries
--------------------------

No matter which installation route you take (see
`Installation Overview`_), we're going to need a directory to place
configuration and audio files. The directions here will assume that you
created a new directory called ``disquip-bot`` in your home directory.
On Windows, that's typically ``C:\Users\<youruser>\disquip-bot``. Please
create this directory before going forward. To keep these directions
simple, this directory will be referred to as ``~/disquip-bot`` going
forward.

Download disquip.ini
^^^^^^^^^^^^^^^^^^^^

Download `disquip.ini`_ and place it in ``~/disquip-bot``. Later, in
`Configuration`_ we'll be modifying this file.

Create "audio_files" Directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create a new directory called ``audio_files`` underneath
``~/disquip-bot``. This is where we'll be placing our quips later on
(`Audio Files`_).


Docker Based Installation
-------------------------

Note that if you're running Windows, you'll need at least Windows 10
version 2004. More details can be found at `Install Docker on Windows`_.

The Docker installation process is simpler for Linux users (and maybe
for Mac users as well?), so no directions are provided here. Head on out
to the `Docker`_ documentation to get started.


Install Docker On Windows
^^^^^^^^^^^^^^^^^^^^^^^^^

How you proceed depends on the edition of Windows 10 you're running. Many
users will likely have Windows Home, and should thus *carefully* follow
the directions at `Install Docker on Windows Home`_. If you have a
Windows edition other than Windows Home, *carefully* follow the
directions at
`Install Docker on Windows Pro, Enterprise, or Education`_.

The easiest way to tell the Windows edition, version, and build you're
running is to type "About" into the Windows search bar, and open
click on the "About your PC" box. In the window that opens, scroll down
to "Windows specifications" to get information about your Windows
installation.

Inevitably, Docker's installation instructions will instruct you to
`Install Windows Subsystem for Linux`_. At the time of writing
(2020-10-11), you can stop after completing "Step 5 - Set WSL 2 as your
default version." No need to move on to "Step 6 - Install you Linux
distribution of choice" unless you would like to.


Download the Disquip Bot Docker Image
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you have Docker installed, it's time to download the Docker image
for Disquip. Open up your favorite terminal (e.g. Command Prompt on
Windows) and enter in the command
``docker pull blthayer/disquip-bot:latest``. You'll now have a runnable
Docker image with all the Disquip Bot prerequisites already installed.

**For Advanced Users**: If you would prefer to build your own Docker
image rather than pull a pre-built one, that is of course an option.
Start by cloning or downloading the repository locally. Then, in your
terminal change directories to the repository and run
``docker_build.bat``. Linux/Mac users should be able to convert this to
a ``.sh`` script in a matter of seconds :) *Additional info*: The main
Dockerfile is simply called ``Dockerfile``. For caching convenience, a
build needs run for both of the Dockerfiles in the ``docker_ffmpeg``
directory. I've hard-coded the Docker repository and tags throughout
the Dockerfiles and helper scripts, and you may wish to change those
when you run your own build.

Local Installation
------------------

Local installation involves installing `Prerequisites`_ and then
installing the Disquip Bot.

Prerequisites
^^^^^^^^^^^^^

TL;DR:

-   `Python`_ >= 3.6
-   `FFmpeg`_
-   `7zip`_
-   **OPTIONAL**: `Notepad++`_

Disquip Bot *should* be operating system agnostic, but to date has only
been tested on Windows (I know, gross.).

Disquip Bot is a Python program and thus requires that you install
`Python`_. Specifically, ensure you are running a version of Python
>= 3.6. Before going any further take a moment to `download Python`_ and
then install it.

For Windows users: later we'll be downloaded a compressed ``.7z``
archive that we'll need to extract. For extraction, we'll use `7zip`_.
Please download and install.

In order to stream audio files over the internet, a handy program
called `FFmpeg`_ is used. Windows users should refer to
`Install FFmpeg (Windows)`_. Mac/Linux users are assumed to be highly
computer literate users who can get FFmpeg working solely given the link
to FFmpeg :) If anyone would like to provide directions for Mac or Linux
I'm happy to add them here.

Install FFmpeg (Windows)
^^^^^^^^^^^^^^^^^^^^^^^^

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

Configure Python Virtual Environment and Install Disquip Bot
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After you've installed Python, we'll be configuring what's known as a
virtual environment to install Python dependencies as well as the
Disquip Bot. Here are directions for Windows (similar on Mac/Linux):

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
6.  Install the Disquip Bot and its dependencies by running
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
is a *very* powerful tool that you could use to create clips.

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

The Disquip bot only needs the following permissions:
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

All the necessary configuration parameters for Disquip Bot are defined
in ``disquip.ini``, which you should have downloaded during the
`Installation Preliminaries`_. Rather than list every configuration
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
To alleviate this, the Disquip Bot supports aliases for commands. Check
out the ``[aliases]`` section of ``disquip.ini``

Run the Bot
-----------

After you've performed all the installation and configuration steps
above, you're ready to run! Running the bot looks different depending
on whether you took the `Docker Based Installation`_ or
`Local Installation`_ path. Read on!

Running for Docker Install
^^^^^^^^^^^^^^^^^^^^^^^^^^

If you're on Windows, download the file called ``docker_run.bat`` from
`Disquip Bot`_ on GitHub and place it in your ``~/disquip-bot``
directory. Simply run the script inside the ``~/disquip-bot`` directory
to fire it up! This script assumes you've placed all files as directed
in these directions. If you didn't, the script will be easy to tweak.
For Mac/Linux users, ``docker_run.bat`` will be very easy to port to
a shell script.

To stop the bot, use the ``Ctrl + C`` keyboard command. Unfortunately,
this will only kill the command window and not the actual Docker
container. Run ``docker container ls`` to view running containers.
Locate the name (``NAMES`` column) of the running container and then
execute ``docker stop <name>``.

Running for Local Install
^^^^^^^^^^^^^^^^^^^^^^^^^

This is pretty quick and easy! :)

1.  Using a command prompt, change directories to ``~/disquip-bot`` via
    ``cd %USERPROFILE%\disquip-bot``.
2.  Activate your virtual environment via the command
    ``venv\Scripts\activate.bat``.
3.  Execute the command ``disquip-bot`` to fire it up.

When you're done, simply kill the command window you have running or
use ``Ctrl + C`` to stop the program.

Updating Configurations or Audio Files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Disquip bot does not dynamically detect changes to audio files or
configurations. After making a change, simply stop the bot and start it
again to pick up any changes.

Using the Bot
-------------

The bot will listen to all the text channels of the server(s) you added
it to and look for messages that start with the ``cmd_prefix`` defined
in ``disquip.ini``. This defaults to the exclamation mark (``!``).

Start exploring!

Help
^^^^

Assuming your command prefix is ``!``, simply type ``!help`` into a
text channel the bot has access to. It'll respond with a listing of
available commands and some other helpful information.

.. _7zip: https://www.7-zip.org/
.. _Age of Empires: https://www.ageofempires.com/
.. _Discord: https://discord.com/
.. _Discord applications: https://discord.com/developers/applications
.. _disquip.ini: https://github.com/blthayer/disquip-bot/blob/main/disquip.ini
.. _Disquip Bot: https://github.com/blthayer/disquip-bot
.. _Disquip Bot .zip archive: https://github.com/blthayer/disquip-bot/archive/main.zip
.. _Disquip Bot via git clone: https://github.com/blthayer/disquip-bot.git
.. _Docker: https://docs.docker.com/
.. _Download Python: https://www.python.org/downloads/
.. _FFmpeg: https://ffmpeg.org/
.. _git-essentials FFmpeg build: https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-essentials.7z
.. _gyan.dev: https://www.gyan.dev/ffmpeg/builds/
.. _Install Docker on Windows Home: https://docs.docker.com/docker-for-windows/install-windows-home/
.. _Install Docker on Windows Pro, Enterprise, or Education: https://docs.docker.com/docker-for-windows/install/
.. _Install Windows Subsystem for Linux: https://docs.microsoft.com/en-us/windows/wsl/install-win10
.. _myinstants.com: https://www.myinstants.com
.. _Notepad++: https://notepad-plus-plus.org/
.. _Python: https://www.python.org/
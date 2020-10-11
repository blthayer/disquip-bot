disquip-bot
***********

An easy-to-use Discord soundboard bot. BYO audio files and quip away!

Introduction
============

The purpose of the Disquip Bot project is to provide a simple
sound board bot that is easy to install, configure, and run. After
installation, simply create a directory structure with your own quips
(audio files) and run the bot! Then, head on over to your favorite
Discord server, and punch in commands like ``!aoe3 11`` and the bot
will play the corresponding quip for you.

If your interest is piqued, you can get moving by checking out
`Installation`_.

Backstory
---------

I found myself wishing I could easily play taunts from the
`Age of Empires <https://www.ageofempires.com/>`__ video games while
playing other games with my friends. So, I built out a prototype that
went by the name of "AOE Taunt Board." Myself and my friends liked it,
so I figured I'd make a publicly distributable version for you, the
reader!

Installation
============

Depending on your personal level of computer literacy, installation
takes ~10-60 minutes. It's possible that in the future this project will
provide a simple .zip download with *everything* you need, reducing
installation time to the 5 minute or less range. However, I'd have to
figure out where to host the installation files for download...

The installation process is roughly:

1.  Install `Prerequisites`_.
2.  Download (or Git clone) the
    `Disquip Bot project <https://github.com/blthayer/disquip-bot>`__.
3.  Set up your `Audio Files`_.
4.  Create an application for your
    `Discord <https://discord.com/developers/applications>`__ account.
5.  Do some simple `Configuration`_.
6.  `Add the bot to servers`_.
7.  `Run the bot`_.
8.  Enjoy!

Prerequisites
-------------

Disquip Bot *should* be operating system agnostic, but to date has only
been tested on Windows (I know, gross.).

Disquip Bot is a Python program and thus requires that you install
`Python <https://www.python.org/>`__. Specifically, ensure you are
running a version of Python >= 3.7. Before going any further take
a moment to `download <https://www.python.org/downloads/>`__ and install
Python if you don't already have it.

In order to stream audio files over the internet, a handy program
called `ffmpeg <https://ffmpeg.org/>`__ is used. Windows users can
check out `Install FFmpeg (Windows)`_. Mac/Linux users are
assumed to be highly computer literate users who can get FFmpeg working
solely given the link to FFmpeg :) If anyone would like to provide
directions for Mac or Linux I'm happy to add them.

Install FFmpeg (Windows)
^^^^^^^^^^^^^^^^^^^^^^^^

Download Disquip Bot Project
----------------------------

Audio Files
===========

Discord Configuration
=====================

Create Discord Application
--------------------------

Add the Bot to Servers
----------------------

Configuration
=============

Run the Bot
===========

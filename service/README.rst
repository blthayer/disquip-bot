service
=======

This directory contains a sample implementation for running the DisQuip
Bot as a Linux systemd service. I was able to host
the bot on a Raspberry Pi 3 Model B running Raspbian (effectively
Debian) 9 (stretch) using these directions, although they should work
for many different Linux variants. More recently, I've hosted the bot on
a Raspberry Pi 4 running Raspbian 11 (bullseye).

All commands in this document are shell commands. As such, you're
assumed to have enough Linux knowledge to run shell commands and edit
files.

Prerequisites
-------------

-   Computer running a modern-ish Linux operating system. Specifically,
    we'll be using:
    -   systemd
    -   rsyslog
    -   logrotate
    -   cron
-   Follow the DisQuip Bot installation instructions for a local
    installation on your Linux machine. Directions here will assume
    you have a Python virtual environment in ``~/disquip-bot/venv``.
    This environment can quickly be created via, *e.g.*,
    ``python3 -m venv ~/disquip-bot/venv``, and the DisQuip Bot should
    be installed in this virtual environment like so:
        -   ``source ~/disquip-bot/venv/bin/activate``
        -   ``python -m pip install disquip-bot``

Installing Python
^^^^^^^^^^^^^^^^^

Often, versions of Python available via your package manager (*e.g.*,
``apt-get`` in Debian/Ubuntu/Raspbian) are relatively old. Additionally,
managing different Python installations and environments can be a real
pain, and you can screw up your system if you aren't careful. See
`xkcd <https://xkcd.com/1987/>`_.

If you wish to install a different version of Python than what ships
with your system, I highly recommend using
`pyenv <https://github.com/pyenv/pyenv>`_ - follow the directions in
their README very carefully (RTFM!), and don't forget to install
`the prerequisites <https://github.com/pyenv/pyenv/wiki#suggested-build-environment>`_.

If you insist on downloading the Python source and building yourself
manually, you can find some directions in the git history of this file.
I don't recommend it.

Directions
----------

Now that we've got the preliminaries out of the way, here are some
step-by-step directions to get the DisQuip Bot running as a systemd
service:

1.  Edit the appropriate sections of ``disquip-bot.service`` according
    to your installation. At the time of writing, the three
    directives that will need your attention are ``ExecStart``,
    ``Environment``, and ``WorkingDirectory``.
2.  Copy the service file for systemd:
    ``sudo cp disquip-bot.service /lib/systemd/system/disquip-bot.service``
3.  Update permissions:
    ``sudo chmod 644 /lib/systemd/system/disquip-bot.service``
4.  Edit ``disquip-bot.rsyslog.conf`` according to your preference for
    log files. The default log location is ``/var/log/disquip-bot.log``.
5.  Copy the rsyslog configuration file:
    ``sudo cp disquip-bot.rsyslog.conf /etc/rsyslog.d/``
6.  Create the log file: ``sudo touch /var/log/disquip-bot.log``
7.  Update the log path in ``disquip-bot.logrotate.conf`` to match
    what's in ``disquip-bot.rsyslog.conf``. If you kept the default,
    no action is needed here.
8.  Copy the logrotate configuration file:
    ``sudo cp disquip-bot.logrotate.conf /etc/logrotate.d/``
9.  Optionally run a logrotate dry run:
    ``logrotate -d /etc/logrotate.d/disquip-bot.logrotate.conf``
10. Reload systemd: ``sudo systemctl daemon-reload``
11. Restart rsyslog: ``sudo systemctl restart rsyslog``
12. Fire up DisQuip Bot: ``sudo systemctl start disquip-bot``
13. Check the bot's status: ``sudo systemctl status disquip-bot``
14. Enable the bot to start up on system boot:
    ``sudo systemctl enable disquip-bot``
15. OPTIONAL: Restart the disquip-bot service daily:
    ``sudo cp disquip-bot /etc/cron.daily/``. The file should already
    be executable, but just in case:
    ``sudo chmod +x /etc/cron.daily/disquip-bot``. Note that the
    ``/etc/cron.daily`` directory is specific to Debian-like distros.
    The bot seems to be stable enough that daily restarts aren't
    strictly necessary, but I have experienced an issue where it got
    hung up due to a connectivity problem.

And that's it! You can now manage DisQuip Bot via systemd/the
``systemctl`` command, and you can find logs at
``/var/log/disquip-bot.log``. Enjoy!

service
=======

This directory contains a sample implementation for running the DisQuip
Bot as a Linux systemd service. DisQuip Bot's author was able to host
the bot on a Raspberry Pi 3 Model B running Raspbian GNU/Linux 9
(stretch) using these directions, although they should work for many
different Linux variants.

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
-   Follow the DisQuip Bot installation instructions for a local
    installation on your Linux machine. Directions here will assume
    you have a Python virtual environment in ``~/disquip-bot/venv``.
    This environment can quickly be created via
    ``python3 -m venv ~/disquip-bot/venv``, and the DisQuip Bot should
    be installed in this virtual environment:
        -   ``source ~/disquip-bot/venv/bin/activate``
        -   ``python3 -m pip install disquip-bot``

Installing Python From Source
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Avoid following these directions if you can. It's much simpler to use
your OS's package manager (e.g. ``apt-get``) to install Python. However,
if you have an older Raspberry Pi like me, the newest available version
of Python that's available via ``apt-get`` is 3.5. I had previously
installed Python 3.6 from source on my Pi, so I figured I'd share my
notes with you here. These directions should work for other versions
of Python as well. Note that building Python from source on an older
Pi will take several hours to complete (though you don't have to be
present for more than 5 minutes of that :)

1.  Install prerequisite libraries:
    ``sudo apt-get install libssl-dev libncurses5-dev libsqlite3-dev libreadline-dev libtk8.5 libgdm-dev libdb4o-cil-dev libpcap-dev zlib1g-dev``
    (`source <https://stackoverflow.com/a/49696062/11052174>`__)
2.  Download Python 3.6 source code:
    ``wget https://www.python.org/ftp/python/3.6.12/Python-3.6.12.tar.xz``
3.  Extract the archive: ``tar -xf Python-3.6.12.tar.xz``
4.  Change directories: ``cd Python-3.6.12``
5.  Configure: ``./configure --enable-optimzations``
6.  Make: ``make -j $(($(nproc) + 1))``
7.  Install: ``sudo make -j $(($(nproc) + 1)) altinstall``
8.  Optional alias: Add the following to ``~/.bash_aliases``:
    ``alias python3='/usr/local/bin/python3.6'``
9.  Create virtual environment: ``python3 -m venv ~/disquip-bot/venv``

Directions
----------

Now that we've got the preliminaries out of the way, here are some
step-by-step directions to get the DisQuip Bot running as a systemd
service:

1.  Edit the appropriate sections of ``disquip-bot.service`` according
    to your installation. At the time of writing, the only two
    directives that will need your attention are ``ExecStart`` and
    ``WorkingDirectory``.
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

And that's it! You can now manage DisQuip Bot via systemd/the
``systemctl`` command, and you can find logs at
``/var/log/disquip-bot.log``. Enjoy!

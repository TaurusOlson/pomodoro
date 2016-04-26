pomodoro
========

**pomodoro** is a simple `Pomodoro`_ timer. 
I use it to keep track of my time when I work and stay productive.


Usage
-----

* Start the timer::

    pomodoro --start

* Stop the timer::

    pomodoro --stop

* Restart the timer::

    pomodoro --restart

* Reinitialize all the pomodori::

    pomodoro --reset

* Print the status::

    pomodoro --status


Features
--------

* Simple
* No dependencies


Installation
------------

* Creating a virtual environment and calling it every time you want to use the
  script, so you can just run the following commands::

    git clone git@github.com:TaurusOlson/pomodoro.git <path/to/pomodoro>
    echo 'alias pomodoro="python <path/to/pomodoro>/pomodoro/cli.py"' >> ~/.zshrc

where ``<path/to/pomodoro>`` is the path to where you want to install the repository.
If you use Bash, replace ``~/.zshrc`` with ``~/.bashrc``.


Limitations
-----------

**pomodoro** has been tested only on Mac OS X. It uses the default audio
player, afplay, to play an audio file used as the ring at the end of
a pomodoro.
I haven't used Linux and Windows for years so I don't know very well the audio
players on these platforms (mplayer, VLC?). I'll take some time to
implement this. If you have an idea, please open an issue or submit a pull
request.


Credits
-------

The ``daemon`` module used in this package comes from `https://github.com/serverdensity/python-daemon`.

.. _pomodoro: http://pomodorotechnique.com/

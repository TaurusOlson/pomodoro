pomodoro
========

**pomodoro** is a simple Pomodoro timer.


Usage
-----

* Start the timer::

    pomodoro --start

* Stop the timer::

    pomodoro --stop

* Restart the timer::

    pomodoro --restart

* Reinitialize all the pomodori  ::

    pomodoro --reset

Features
--------

* Simple
* No dependencies


Installation
------------

* With pip in a virtual environment::

    pip install pomodoro

* Creating a virtual environment and calling it every time you want to use the
  script, so you can just run the following commands::

    git clone git@github.com:TaurusOlson/pomodoro.git <path/to/pomodoro>
    echo 'alias pomodoro="python <path/to/pomodoro>/pomodoro/cli.py"' >> ~/.zshrc

where `<path/to/pomodoro>` is the path to where you want to install the repository.
If you use Bash, replace `~/.zshrc` with `~/.bashrc`


Acknowledgement
---------------

The `daemon` module used in this package comes from `https://github.com/serverdensity/python-daemon`.


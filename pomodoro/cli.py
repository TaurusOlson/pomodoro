#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cli

A Pomodoro timer in command line

:copyright: (c) 2016 by Taurus Olson <taurusolson@gmail.com>
:license: MIT

"""

import time
import itertools
import os
import sys
import argparse
from daemon import Daemon


# INPUTS {{{1
DEFAULT_ALARM_FILE = '/System/Library/Sounds/Submarine.aiff'
DEFAULT_PID_FILE = '/tmp/pomodoro-daemon.pid'
DEFAULT_POMODORO_FILE = os.path.expanduser("~/.pomodoro.txt")
DEFAULT_PLAYER = 'afplay -v 100'


# The POMODORO_FILE is written after the execution of the current pomodoro. 
# It contains the index of the next pomodoro.
POMODORO_FILE = DEFAULT_POMODORO_FILE

# Pomodoro pattern
# (25, 5, 25, 5, 25, 5, 25, 20)


# THE DAEMON {{{1
class PomodoroDaemon(Daemon):
    DURATIONS = (25, 5, 25, 5, 25, 5, 25, 20)

    def __init__(self, pid_file=DEFAULT_PID_FILE,
            pomodoro_file=DEFAULT_POMODORO_FILE,
            alarm_file=DEFAULT_ALARM_FILE, verbose=0):
        super(PomodoroDaemon, self).__init__(pid_file, verbose=verbose)
        self.pid_file      = pid_file
        self.pomodoro_file = os.path.expanduser(pomodoro_file)
        self.alarm_file    = os.path.expanduser(alarm_file)
        self.index         = None
        self.duration      = None
        self._status       = None
        self.read_file()

    @property
    def status(self):
        """Return the current status"""
        work_msg = 'Work for {minute} minutes.'.format
        short_break_msg = 'Time for a short break ({minute} minutes)'.format
        long_break_msg = 'You deserve a long break ({minute} minutes)'.format

        if self.duration == 25:
            cur_status = work_msg(minute=self.duration)
        elif self.duration == 5:
            cur_status = short_break_msg(minute=self.duration)
        elif self.duration == 20:
            cur_status = long_break_msg(minute=self.duration)
        return cur_status

    @status.setter
    def status(self, new_status):
        """Set the current status"""
        self._status = new_status

    def read_file(self):
        """Read filename if it exists"""
        if os.path.exists(self.pomodoro_file):
            with open(self.pomodoro_file, 'r') as f:
                data = f.readline()
                self.index = int(data)
        else:
            self.index = 0
        self.duration = PomodoroDaemon.DURATIONS[self.index]

    def write_file(self):
        """Write the next index into the pomodoro file"""
        with open(self.pomodoro_file, 'w') as f:
            next_index = (self.index+1) % len(PomodoroDaemon.DURATIONS)
            f.write('{next_index}'.format(next_index=next_index))

    def print_status(self):
        """Print the current status if there is an ongoing pomodoro.

        Otherwise print the next status.
        """
        data = {'status': self.status,
                'cur': self.index + 1,
                'total': len(PomodoroDaemon.DURATIONS)}
        if os.path.exists(self.pid_file):
            print '\nCurrent status: [{cur}/{total}] {status}\n'.format(**data)
        else:
            print '\nNext status: [{cur}/{total}] {status}\n'.format(**data)

    def run(self):
        """Run the timer and play a sound when it's finished"""
        self.print_status()
        time.sleep(self.duration * 60)
        os.system('{player} {mp3_file}'.format(player=DEFAULT_PLAYER, mp3_file=self.alarm_file))
        self.write_file()

    def reset(self):
        """Reset the Pomodoro pattern from the beginning"""
        if os.path.exists(self.pomodoro_file):
            os.remove(self.pomodoro_file)


def main():
    pomodoro_daemon = PomodoroDaemon()

    parser = argparse.ArgumentParser(description='A Pomodoro timer in command line')
    parser.add_argument('--start', action='store_true', help='Start the timer')
    parser.add_argument('--stop', action='store_true', help='Stop the timer')
    parser.add_argument('--restart', action='store_true', help='Restart the timer')
    parser.add_argument('--reset', action='store_true', help='Erase all the pomodori')
    parser.add_argument('--status', action='store_true', help='Display the status')
    args = parser.parse_args()

    if args.start:
        pomodoro_daemon.start()
    elif args.stop:
        pomodoro_daemon.stop()
    elif args.restart:
        pomodoro_daemon.restart()
    elif args.reset:
        pomodoro_daemon.reset()
    elif args.status:
        pomodoro_daemon.print_status()
    else:
        parser.print_help()
        sys.exit(2)
    sys.exit(0)


# RUN THE TIMER {{{1
if __name__ == '__main__':
    main()

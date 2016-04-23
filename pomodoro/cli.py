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
        self.cur_index = 0
        self.pomodoro_file = os.path.expanduser(pomodoro_file)
        self.alarm_file = os.path.expanduser(alarm_file)
        self.cur_duration = PomodoroDaemon.DURATIONS[self.cur_index]

    def read_file(self):
        """Read filename if it exists"""
        if os.path.exists(self.pomodoro_file):
            with open(self.pomodoro_file, 'r') as f:
                data = f.readline()
                self.cur_index = int(data)
        else:
            self.cur_index = 0

    def write_file(self):
        with open(self.pomodoro_file, 'w') as f:
            next_index = (self.cur_index+1) % len(PomodoroDaemon.DURATIONS)
            f.write('{next_index}'.format(next_index=next_index))

    def print_msg(self):
        work_msg = 'Work for {minute} minutes.'.format
        short_break_msg = 'Time for a short break ({minute} minutes)'.format
        long_break_msg = 'You deserve a long break ({minute} minutes)'.format

        if self.cur_duration == 25:
            print work_msg(minute=self.cur_duration)
        elif self.cur_duration == 5:
            print short_break_msg(minute=self.cur_duration)
        elif self.cur_duration == 20:
            print long_break_msg(minute=self.cur_duration)

    def run(self):
        self.read_file()
        self.cur_duration = PomodoroDaemon.DURATIONS[self.cur_index]
        self.print_msg()
        time.sleep(self.cur_duration * 60)
        os.system('afplay -v 100 {mp3_file}'.format(mp3_file=self.alarm_file))
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
    args = parser.parse_args()

    if args.start:
        pomodoro_daemon.start()
    elif args.stop:
        pomodoro_daemon.stop()
    elif args.restart:
        pomodoro_daemon.restart()
    elif args.reset:
        pomodoro_daemon.reset()
    else:
        parser.print_help()
        sys.exit(2)
    sys.exit(0)


# RUN THE TIMER {{{1
if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-

"""
setup

:copyright: (c) 2016 by Taurus Olson <taurusolson@gmail.com>
:license: MIT

"""

from setuptools import setup
import pomodoro 

setup(
        name='pomodoro',
        version=pomodoro.__version__,
        author='Taurus Olson',
        author_email='taurusolson@gmail.com',
        description='A Pomodoro timer in command line',
        platforms='',
        entry_points='''
        [console_scripts]
        pomodoro=pomodoro.cli:main
        '''
)

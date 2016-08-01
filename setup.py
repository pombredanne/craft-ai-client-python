#!/usr/bin/env python

from distutils.core import setup

setup(name='craft-ai',
      version='0.1',
      description='craft ai API client for python',
      author='craft.ai team',
      author_email='contact@craft.ai',
      url='https://github.com/craft-ai/craft-ai-client-python/',
      packages=['craftai'],
      requires=['requests', 'six']
      )

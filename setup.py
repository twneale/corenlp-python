#!/usr/bin/env python
from setuptools import setup, find_packages


long_description = ''

setup(name='corenlp',
      version='0.0',
      packages=find_packages(),
      author='Thom Neale',
      author_email='twneale@gmail.com',
      url='http://github.com/twneale/corenlp-python',
      license='MIT',
      description='Object-oriented wrapper for Core NLP XML',
      long_description=long_description,
      platforms=['any'],
)

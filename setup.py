#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup
#from distutils.core import setup

version = '0.4'

path = os.path.dirname(__file__)
if not path: path = '.'
readme = open(path + '/README.rst', 'r').read()

setup(name='django-selector',
      version=version,
      description=readme.split('\n')[0],
      long_description=readme,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Operating System :: OS Independent',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
      ],
      keywords='django urls',
      author='Jason Moiron',
      author_email='jmoiron@jmoiron.net',
      url='http://dev.jmoiron.net/hg/django-selector/',
      license='MIT',
      #packages=['argot'],
      #scripts=['bin/argot'],
      # setuptools specific
      zip_safe=False,
      test_suite = "tests",
      # i'm not sure how to get my virtualenv or setuptools to realize that
      # there is a perfectly fine system-wide lxml library available; until
      # i fix that, there won't be a "hard" requirement, even though lxml is
      # 100% required for argot to function
      install_requires=[] # , 'lxml'],
)



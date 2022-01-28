# -*- coding: utf-8 -*-
"""
$Id: setup.py 1 2022-01-28 11:52:17Z aokada $
"""

from setuptools import setup
from scripts.ecsub2qsub import __version__

import sys
sys.path.append('./tests')

setup(name='ecsub2qsub',
      version=__version__,
      description="ecsub2qsub is a command-line tool to qsub scripts of ecsub.",
      long_description="""""",

      classifiers=[
          #   3 - Alpha
          #   4 - Beta
          #   5 - Production/Stable
          'Development Status :: 3 - Alpha',
          # Indicate who your project is intended for
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Bio-Informatics',
          'Topic :: Scientific/Engineering :: Information Analysis',

          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
      ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      
      keywords=' cloud bioinformatics',
      author='Ai Okada',
      author_email='aokada@ncc.go.jp',
      url='https://github.com/aokad/ecsub2qsub.git',
      license='GPLv3',
      
      package_dir = {'': 'scripts'},
      packages=['ecsub2qsub'],
      scripts=['ecsub2qsub'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'pytz',
          'six'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      package_data = {
      }
)

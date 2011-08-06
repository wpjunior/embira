#-*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

DESCRIPTION = "Event driven network library for python"

def get_version(version_tuple):
    version = '%s.%s' % (version_tuple[0], version_tuple[1])
    if version_tuple[2]:
        version = '%s.%s' % (version, version_tuple[2])
    return version

init = os.path.join(os.path.dirname(__file__), 'embira', '__init__.py')
version_line = filter(lambda l: l.startswith('VERSION'), open(init))[0]
VERSION = get_version(eval(version_line.split('=')[-1]))

CLASSIFIERS = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Topic :: System :: Networking',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

setup(name='embira',
      version=VERSION,
      packages=find_packages(),
      author='Wilson Júnior',
      author_email='wilsonpjunior@{nospam}gmail.com',
      url='http://wpjunior.github.com/embira/',
      license='GPL',
      include_package_data=True,
      description=DESCRIPTION,
      platforms=['any'],
      classifiers=CLASSIFIERS,
      test_suite='tests',
)

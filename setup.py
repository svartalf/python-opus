# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='opus',
    version='0.0.1',
    author='SvartalF',
    author_email='self@svartalf.info',
    url='https://github.com/svartalf/python-opus',
    description='Python bindings to the libopus, IETF low-delay audio codec',
    packages=('opus', 'opus.api'),
    test_suite='tests',
    classifiers=(
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Multimedia :: Sound/Audio :: Conversion',
    ),
)

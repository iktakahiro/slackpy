#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

__author__ = 'Takahiro Ikeuchi'


setup(
    name="slackpy",
    version="1.1.0",
    py_modules=['slackpy'],
    package_dir={'': 'slackpy'},
    install_requires=open('requirements.txt').read().splitlines(),
    description="Simple Slack client library",
    long_description=open('README.txt').read(),
    author='Takahiro Ikeuchi',
    author_email='takahiro.ikeuchi@gmail.com',
    url='https://github.com/iktakahiro/slackpy',
    keywords=["Slack", "Slack Client"],
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.4",
        "Topic :: System :: Logging",
        "Topic :: Communications :: Chat"
    ],
    entry_points={
        "console_scripts": [
            "slackpy=slackpy:main",
        ],
    },
)


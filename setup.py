#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

__author__ = 'Takahiro Ikeuchi'

requires = ['requests']
test_requirements = ['requests', 'pytest']
extras_requires = {
    ':python_version<"3.4"': ["enum34"],
}

setup(
    name="slackpy",
    version="1.4.0",
    py_modules=['slackpy', 'commandline'],
    package_dir={'': 'slackpy'},
    install_requires=requires,
    extras_require=extras_requires,
    description="Simple and Useful Slack client library",
    long_description=open('README.rst').read(),
    author='Takahiro Ikeuchi',
    author_email='takahiro.ikeuchi@gmail.com',
    url='https://github.com/iktakahiro/slackpy',
    keywords=["Slack", "Slack Client"],
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 2.7",
        "Topic :: System :: Logging",
        "Topic :: Communications :: Chat"
    ],
    entry_points={
        "console_scripts": [
            "slackpy=commandline:main",
        ],
    },
    tests_require=test_requirements
)

#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Allow trove classifiers in previous python versions
from sys import version
if version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None

from nasne import __version__ as version

def requireModules(moduleNames=None):
    import re
    if moduleNames is None:
        moduleNames = []
    else:
        moduleNames = moduleNames

    commentPattern = re.compile(r'^\w*?#')
    moduleNames.extend(
        filter(lambda line: not commentPattern.match(line),
            open('requirements.txt').readlines()))

    return moduleNames

setup(
    name='nasne',
    version=version,

    author='garaemon',
    author_email='garaemon@gmail.com',

    description='Python interface for nasne',
    long_description=open('README.txt').read(),
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers'
    ],
    keywords='nasne',

    install_requires=requireModules([

    ]),
    packages=['nasne'],

    url='https://github.com/garaemon/python-nasne',
    test_suite='nasne'
)

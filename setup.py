from setuptools import setup, command

import os
import sys
import tarfile
import urllib


def download_mallet():
    url = "mallet.cs.umass.edu/dist/mallet-2.0.7.tar.gz"
    local_jar_dir = "ext"
    print >> sys.stderr, "Downloading", url
    tgz_filepath, headers = urllib.urlretrieve(url)
    print >> sys.stderr, 'Opening', tgz_filepath



setup(
    name="pymallet",
    version=str(package['version']),
    packages=['pymallet'],
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
        ],
    },
    cmdclass={
        'install_mallet': download_mallet
    }
)
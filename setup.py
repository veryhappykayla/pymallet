from setuptools import setup, command, find_packages

import os
import sys
import tarfile
import urllib

readme = open('README.txt').read()


def download_mallet():
    pass

    url = "mallet.cs.umass.edu/dist/mallet-2.0.7.tar.gz"
    local_jar_dir = "ext"
    print >> sys.stderr, "Downloading", url
    tgz_filepath, headers = urllib.urlretrieve(url)
    print >> sys.stderr, 'Opening', tgz_filepath


setup(
    name="pymallet",
    # version=str(package['version']),
    version='0.1',
    author='Nathan Leiby',
    author_email='nathanleiby@gmail.com',
    license='MIT',
    description='Mallet (natural language processing) wrapper in Python',
    long_description=readme,
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

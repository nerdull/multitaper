# PyPI setup file
# thanks to https://stackoverflow.com/a/23265673/5177935
#

from setuptools import setup, find_packages
from multitaper.version import __version__

long_description = ''

try:
    from pypandoc import convert

    def read_md(f): return convert(f, 'rst', 'md')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")

    def read_md(f): return open(f, 'r').read()

classifiers = [
    'Environment :: Console',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Topic :: Scientific/Engineering :: Physics',
    'Topic :: Software Development :: Libraries',
]

setup(
    name='multitaper',
    packages=find_packages(),
    version=__version__,
    description='A simple pure python implementation of the multitaper spectral density estimator.',
    long_description=read_md('README.md'),
    author='nerdull',
    url='https://github.com/nerdull/multitaper',  # use the URL to the github repo
    download_url='https://github.com/nerdull/multitaper/tarball/{}'.format(__version__),
    license='GPLv3',
    keywords=['physics', 'data', 'time series', 'spectral density estimation'],  # arbitrary keywords
    classifiers=classifiers
)

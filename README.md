# multitaper
A pure Pythonic implementation of the *multitaper* method for spectral density estimation. It takes a 1D or 2D **numpy.ndarray** as the input and estimates its power spectral density. Each time an object is created, a new Slepian sequence is generated. This object can be used to calculate power spectral density as often as possible.

## Prerequisites
This code depends only on `numpy` and `scipy` so it works with Python version 2 and 3 (tested with versions 2.7.15 and 3.6.5).

## Installation

You can install this library by typing:

    python setup.py install --record installed_files.txt

This may or may not need `sudo` depending on your installation. The last argument helps you track files that are installed on your system, in case you like to remove them later.

## Similar projects
Other libraries including a multitaper implementations for Python can be found on PyPI are [mtspec](https://pypi.org/project/mtspec/), [libftr](https://pypi.org/project/libtfr/) and [spectrum](https://pypi.org/project/spectrum/).

## Further Reading

* Percival, D. B. and Walden, A. T., Spectral Analysis for Physical Applications, Cambridge University Press 2002, ISBN: [9780521435413](http://www.worldcat.org/oclc/803678734)

## License
**MIT**

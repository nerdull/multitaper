#!/usr/bin/env python3
# −*− coding:utf-8 −*−

import numpy as np
from scipy.linalg import eigh_tridiagonal


class Multitaper(object):
    '''
    A class to perform the spectral density estimation of an input signal based on the multitaper method
    '''

    def __init__(self, nn, nw=3.5, kk=7):
        '''
        Initialize the object.
        nn:     taper length
        nw:     half of resolution bandwidth
        kk:     number of tapers, in principle less than 2*nw
        '''

        self.kk = kk
        self.nw = nw
        self.nn = nn
        self.dpss = self._regen_dpss()

    def __str__(self):
        return "No. of tapers: {}, taper length: {}, half res. BW: {}".format(self.kk, self.nn, self.nw)

    def _regen_dpss(self):
        '''
        The generated tapers in 2D array [[taper_0], [taper_1], ...] are ordered decreasingly by their respective eigenvalues.
        '''
        ww = self.nw / self.nn
        diag_main = ((self.nn - 1) / 2 - np.arange(self.nn))**2 * np.cos(2 * np.pi * ww)
        diag_off = np.arange(1, self.nn) * np.arange(self.nn - 1, 0, -1) / 2
        vecs = eigh_tridiagonal(diag_main, diag_off, select='i', select_range=(self.nn - self.kk, self.nn - 1))[1]
        # polarity follows Slepian convention
        return (vecs * np.where(vecs[0, :] > 0, 1, -1)).T[::-1]

    def estimate(self, signal, axis=-1):
        '''
        Estimate the power spectral density of the input signal.
        signal: n-dimensional array of real or complex values
        axis:   axis along which to apply the Slepian windows. Default is the last one.
        '''
        # conversion to positive-only index
        axis_p = (axis + signal.ndim) % signal.ndim
        sig_exp_shape = list(signal.shape[:axis]) + [1] + list(signal.shape[axis:])
        tap_exp_shape = [1] * axis_p + list(self.dpss.shape) + [1] * (signal.ndim-1-axis_p)
        signal_tapered = signal.reshape(sig_exp_shape) * self.dpss.reshape(tap_exp_shape)
        return np.fft.fftshift(np.mean(np.absolute(np.fft.fft(signal_tapered, axis=axis_p+1))**2, axis=axis_p), axes=axis_p)

# ------------------------


if __name__ == '__main__':
    mymtm = Multitaper(2048)
    sig = np.vectorize(complex)(np.random.rand(2048), np.random.rand(2048))
    print(mymtm.estimate(sig))
    mymtm = Multitaper(256)
    sig = np.reshape(sig, (8, 256))
    print(mymtm.estimate(sig))

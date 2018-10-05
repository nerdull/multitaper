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
        Initialize the object
        nn:  taper length
        nw: half of resolution bandwidth
        kk:  number of tapers, in principle less than 2*nw
        '''

        self.kk = kk
        self.nw = nw
        self.nn = nn
        self.dpss = self._regen_dpss()

    def __str__(self):
        return "Num. of tapers: {}, taper length: {}, res. BW.: {}".format(self.kk, self.nn, self.nw)

    def _regen_dpss(self):
        '''
        The generated tapers in 2D array [[taper_0], [taper_1], ...] are ordered decreasingly by their respective eigenvalues.
        '''
        ww = self.nw / self.nn
        diag_main = ((self.nn - 1) / 2 - np.arange(self.nn)
                     )**2 * np.cos(2 * np.pi * ww)
        diag_off = np.arange(1, self.nn) * np.arange(self.nn - 1, 0, -1) / 2
        vecs = eigh_tridiagonal(diag_main, diag_off,
                                select='i', select_range=(self.nn - self.kk, self.nn - 1))[1]
        # polarity follows Slepian convention
        return (vecs * np.where(vecs[0, :] > 0, 1, -1)).T[::-1]

    def estimate_1d(self, signal):
        '''
        Estimate the power spectral density of the signal in 1D.
        signal: 1D array of real or complex values
        '''
        signal_tapered = signal * self.dpss
        spectrum = np.mean(np.absolute(np.fft.fftshift(
            np.fft.fft(signal_tapered)))**2, axis=0)
        return spectrum

    def estimate_2d(self, signal):
        '''
        Estimate the power spectral density of the signal in 2D.
        signal: 2D array of real or complex value: [[segment_0], [segment_1], ...]
        '''
        signal_tapered = signal[np.newaxis, :, :] * self.dpss[:, np.newaxis, :]
        spectrogram = np.mean(np.absolute(np.fft.fftshift(
            np.fft.fft(signal_tapered), axes=-1))**2, axis=0)
        return spectrogram

# ------------------------


if __name__ == '__main__':
    mymtm = Multitaper(2048)
    sig = np.vectorize(complex)(np.random.rand(2048), np.random.rand(2048))
    print(mymtm.estimate_1d(sig))
    mymtm = Multitaper(256)
    sig = np.reshape(sig, (8, 256))
    print(mymtm.estimate_2d(sig))

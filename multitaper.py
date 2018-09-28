#!/usr/bin/env python3
# −*− coding:utf-8 −*−

import numpy as np
from scipy.linalg import eigh_tridiagonal

class Multitaper(object):
    '''
    A class to perform the spectral density estimation of an input signal based on the multitaper method
    '''

    def gen_dpss(self, N, NW, K):
        '''
        The generated tapers in 2D array [[taper_0], [taper_1], ...] are ordered decreasingly by their respective eigenvalues.
        N:  taper length
        NW: half of resolution bandwidth
        K:  number of tapers, in principle less than 2*NW
        '''
        W = NW / N
        diag_main = ((N-1)/2-np.arange(N))**2 * np.cos(2*np.pi*W)
        diag_off = np.arange(1, N) * np.arange(N-1, 0, -1) / 2
        vecs = eigh_tridiagonal(diag_main, diag_off, select='i', select_range=(N-K,N-1))[1]
        self.dpss = (vecs * np.where(vecs[0,:]>0, 1, -1)).T[::-1] # polarity follows Slepian convention

    def estimate_1d(signal, NW, K):
        '''
        Estimate the power spectral density of the signal in 1D.
        signal: 1D array of real or complex value
        NW:     half of resolution bandwidth
        K:      number of tapers, in principle less than 2*NW
        '''
        self.gen_dpss(signal.size, NW, K)
        signal_tapered = signal * self.dpss
        spectrum = np.mean(np.absolute(np.fft.fftshift(np.fft.fft(signal_tapered)))**2, axis=0)
        return spectrum

    def estimate_2d(signal, NW, K):
        '''
        Estimate the power spectral density of the signal in 2D.
        signal: 2D array of real or complex value: [[segment_0], [segment_1], ...]
        NW:     half of resolution bandwidth
        K:      number of tapers, in principle less than 2*NW
        '''
        self.gen_dpss(signal.size, NW, K)
        signal_tapered = signal[np.newaxis,:,:] * self.dpss[:,np.newaxis,:]
        spectrogram = np.mean(np.absolute(np.fft.fftshift(np.fft.fft(signal_tapered), axes=-1))**2, axis=0)
        return spectrogram

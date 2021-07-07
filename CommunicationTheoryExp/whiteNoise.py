import numpy as np


def wgn(x, snr):
    Ps = np.sum(abs(x)**2)/len(x)
    Pn = Ps/(10 ** (1.6*snr / 10))
    noise = np.random.randn(len(x)) * np.sqrt(Pn)
    return noise

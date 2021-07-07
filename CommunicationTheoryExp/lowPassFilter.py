import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import butter, lfilter, freqz, filtfilt


def butter_lowpass(cutOff, fs, order=5):
    """

    :param cutOff: 截至频率
    :param fs: 采样频率
    :param order: 阶数
    :return:
    """
    nyq = 0.5 * fs
    normalCutoff = cutOff / nyq
    b, a = butter(N=order, Wn=normalCutoff)
    # butter(N, Wn, btype='low', analog=False, output='ba', fs=None)
    return b, a


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(N=order, Wn=[low, high], btype='band')
    return b, a


def butter_lowpass_filter(data, cutOff, fs, order=5):
    b, a = butter_lowpass(cutOff, fs, order=order)
    # y = lfilter(b, a, data)   # 有时延的滤波
    y = filtfilt(b, a, data)  # 没有时延的滤波
    return y


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)
    return y


def lpfDataOnly(order, fs, cutoff, data):
    """
    应用低通滤波器后的波形输出。
    :param order: filter的阶数
    :param fs:采样频率
    :param cutoff:截止频率
    :param data:要过滤的波形数据
    :return: y,t
    """

    t = np.linspace(0, 1, fs, endpoint=False)  # "Noisy" data. We want to recover the 1.2 Hz signal from this.
    y = butter_lowpass_filter(data, cutoff, fs, order)

    return y, t


def bpfDataOnly(order, fs, cutoff1, cutoff2, data):
    """
    应用低通滤波器后的波形输出。
    :param order: filter的阶数
    :param fs:采样频率
    :param cutoff1:截止频率1
    :param cutoff2:截止频率2
    :param data:要过滤的波形数据
    :return: y,t
    """

    t = np.linspace(0, 1, fs, endpoint=False)
    y = butter_bandpass_filter(data, cutoff1, cutoff2, fs, order)

    return y, t

import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import periodogram


def fft_waveform(waveform, length, Fs, N):
    """
    :param waveform: list,需要处理的波形
    :param length: int,信息序列长度
    :param Fs: 采样速率
    :param N: 采样点数/码元
    :return: timeLine, fft_single, f_single
    """
    # timeLine = []
    t = length * N / Fs
    timeLine = np.arange(0, t, 1 / Fs)
    num_fft = len(waveform)
    fft_single = np.abs(np.fft.fft(waveform, num_fft))  # 进行傅里叶变换，前者为数据，后者为数据长度
    f_single = np.arange(num_fft)[range(int(len(timeLine) / 2))] / t
    # fft_single = np.abs(fft_single[1:1 + int((len(waveform)) / 2)]) / num_fft
    fft_single = np.abs(fft_single[range(int(len(fft_single) / 2))]) / num_fft
    return timeLine, fft_single, f_single


def analyse_single(inputS, duty, Fs, f, isSingle=1):
    """
    Parameters
    ----------
    inputS: str
        输入的单or双极性归零码
    duty: float
        正占空比
    Fs: int
        采样速率
    f: int
        码元速率
    isSingle: bool
        是单极性，isSingle=1；是双极性，isSingle=0
        默认为1

    Returns
    -------
    output: List
        输出的用来显示用的List，纵轴
    timeLine: List
        输出的用来显示用的List，横轴
    fft_single: List
        信号进行fft变换后的List
    f_single: List
        频谱的横轴
    """
    output = []
    len_inputS = len(inputS)  # 读取输入序列的长度
    N = int(Fs / f)  # 每个码元的采样点数
    N_high = int(duty * N)  # 高电平所占点数
    for i in range(0, len_inputS):
        if inputS[i] == '1':
            for j in range(i * N, i * N + N_high):  # 码元开始时开始到duty%结束
                output.append(1)  # 输出1
            for j in range(i * N + N_high, (i + 1) * N):
                output.append(0)  # 输出0
        else:
            if isSingle:
                for j in range(i * N, (i + 1) * N):
                    output.append(0)
            else:
                for j in range(i * N, i * N + N_high):
                    output.append(-1)
                for j in range(i * N + N_high, (i + 1) * N):
                    output.append(0)  # 输出0

    timeLine, fft_single, f_single = fft_waveform(output, len_inputS, Fs, N)
    return output, timeLine, fft_single, f_single


def analyse_show(listIn, Fs, f):
    """
    :param listIn: 需要显示出波形的list输入
    :param Fs: 采样频率
    :param f: 码元速率
    :return:output, timeLine, fft_single, f_single

    """
    output = []
    len_listIn = len(listIn)
    N = int(Fs / f)
    i = 0
    for code in listIn:
        for j in range(i * N, (i + 1) * N):
            output.append(code)
        i += 1
    timeLine, fft_single, f_single = fft_waveform(output, len_listIn, Fs, N)
    return output, timeLine, fft_single, f_single


def drawTheGraph(wave_single, timeLine, fft_single, f_single, Fs, title="Waveform Graph"):
    """
    画图函数
    :param wave_single: 用来显示用的List，纵轴
    :param timeLine: 用来显示用的List，横轴
    :param fft_single: 信号进行fft变换后的List
    :param f_single: 频谱的横轴
    :param Fs: 采样率
    :param title: graph's title
    :return: N/A
    """
    f_Pxx, Pxx = periodogram(wave_single, Fs)
    plt.figure(figsize=(8, 8), dpi=80)
    plt.suptitle(title, fontsize=13, fontweight=0, color='black', style='italic', y=0.95)
    # 两幅图像分开输出
    plt.subplot(311)
    plt.xlabel("SIGNAL")
    plt.ylabel("AMP")
    plt.plot(timeLine, wave_single)
    plt.subplot(312)
    plt.grid(True, linestyle='-.')
    plt.xlabel("FREQ")
    plt.ylabel("power_spectrum")
    plt.semilogy(f_Pxx, Pxx)
    plt.subplot(313)
    plt.grid(True, linestyle='-.')
    plt.xlabel("FREQ")
    plt.ylabel("FFT")
    plt.plot(f_single, fft_single)
    plt.show()
    print("图像已输出")
    return

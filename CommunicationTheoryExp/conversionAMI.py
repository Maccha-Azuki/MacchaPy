import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import periodogram

from squareWave import analyse_show, drawTheGraph


def ori_ami(num=24, isManual=0):
    """
    :param isManual: 手动输入消息序列
    :param num: int, 产生消息序列长度
    :return: ami_signal：list，ami码
    """

    if isManual:
        # ori_signal = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ori_signal = [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0]
        num = len(ori_signal)
    else:
        ori_signal = np.random.randint(0, 2, num)  # 产生num位随机二进制码
    am_signal = []
    print("ORIGINAL:", ori_signal)
    count_1 = 0
    # 转换为AMI码
    for i in range(0, len(ori_signal)):
        if ori_signal[i] == 1:
            count_1 += 1
            if count_1 % 2 == 0:
                am_signal.append(ori_signal[i])
            else:
                am_signal.append(-ori_signal[i])
        else:
            am_signal.append(-ori_signal[i])
    return am_signal


def ami_show(Fs, num=24, isManual=0):
    amiList = ori_ami(num, isManual)
    output, timeLine, fft_single, f_single = analyse_show(amiList, 500, 10)
    drawTheGraph(output, timeLine, fft_single, f_single, Fs, "AMI GRAPH")
    return


def ami_hdb3(am_signal):
    count_0 = 0
    hdb3_signal = []
    for j in range(len(am_signal)):
        if am_signal[j] == 0:
            count_0 += 1
            if count_0 == 4:
                hdb3_signal.append(5)
                count_0 = 0
            else:
                hdb3_signal.append(am_signal[j])
        else:
            count_0 = 0
            hdb3_signal.append(am_signal[j])

    count_v = 0
    tmp = 0
    for k in range(len(hdb3_signal)):
        if hdb3_signal[k] == 5:
            count_v += 1
            if count_v == 1 and hdb3_signal[k - 4] is not None:
                hdb3_signal[k] = hdb3_signal[k - 4]
                tmp = hdb3_signal[k]
            else:
                if hdb3_signal[k - 4] == tmp:
                    hdb3_signal[k - 3] = -tmp
                    hdb3_signal[k] = hdb3_signal[k - 3]
                    tmp = hdb3_signal[k]
                else:
                    hdb3_signal[k] = hdb3_signal[k - 4]
                    tmp = hdb3_signal[k]
    i = 0
    for code in hdb3_signal:
        if np.abs(code) == 5:
            hdb3_signal[i] = int(code / 5)
        i += 1
    # print("HDB3:", hdb3_signal)
    return hdb3_signal


def ami_hdb3show(num=24, Fs=500, f=10, isManual=0):
    amiList = ori_ami(num, isManual)
    hdb3List = ami_hdb3(amiList)
    output, timeLine, fft_single, f_single = analyse_show(amiList, Fs, f)
    drawTheGraph(output, timeLine, fft_single, f_single, Fs, "AMI GRAPH")
    output, timeLine, fft_single, f_single = analyse_show(hdb3List, Fs, f)
    drawTheGraph(output, timeLine, fft_single, f_single, Fs, "HDB3 GRAPH")
    return


def powerSpec_Calculate():
    f_Pxx = []
    Pxx_remain_AMI = []
    Pxx_remain_HDB3 = []
    f = 100
    Fs = 1000
    N = int(Fs / f)
    times = 100
    for i in range(int(Fs / 2) + 1):
        Pxx_remain_AMI.append(0)
        Pxx_remain_HDB3.append(0)

    for calculate_time in range(times):
        ami_random_signal = ori_ami(num=f)
        hdb3_random_signal = ami_hdb3(ami_random_signal)
        ami_random_signal_Fs = []
        hdb3_random_signal_Fs = []

        for i in ami_random_signal:
            for j in range(N):
                ami_random_signal_Fs.append(i)

        for i in hdb3_random_signal:
            for j in range(N):
                hdb3_random_signal_Fs.append(i)

        f_Pxx, Pxx_AMI = periodogram(ami_random_signal_Fs, Fs)
        f_Pxx, Pxx_HDB3 = periodogram(hdb3_random_signal_Fs, Fs)
        for k in range(len(Pxx_AMI)):
            Pxx_remain_AMI[k] += Pxx_AMI[k] / times
            Pxx_remain_HDB3[k] += Pxx_HDB3[k] / times
    plt.suptitle("功率谱密度", fontsize=13, fontweight=0, color='black', style='italic', y=0.95)
    plt.subplot(211)
    plt.xlabel("AMI")
    plt.semilogy(f_Pxx, Pxx_remain_AMI)
    plt.subplot(212)
    plt.xlabel("HDB3")
    plt.semilogy(f_Pxx, Pxx_remain_HDB3)

import matplotlib.pyplot as plt
import numpy as np
from squareWave import drawTheGraph, fft_waveform
import whiteNoise as wN
import lowPassFilter as lpf
# import math
import matlab.engine

eng = matlab.engine.start_matlab()


def BPSK():
    plt.figure(figsize=(8, 14), dpi=80)
    plt.subplot(211)
    plt.title("Modulating signal")
    print("仿真图窗1s")
    # f = int(input("请输入码元数(码元速率）："))
    f = 50
    # N = int(input("请输入每个码元的采样点数："))
    N = 2000
    t = np.linspace(0, f, f * N)  # 时间轴
    y = np.ones((f, N), int)
    mt = []
    for i in range(f):
        r_code = int(round(np.random.random()))
        y[i] = r_code * 2 - 1  # 双极性
        mt.append(r_code * 2 - 1)
    y = y.flatten()  # 降维
    plt.grid(True, linestyle='-.')
    plt.plot(t, y, linewidth=1, linestyle="-")  # 绘制
    plt.locator_params(nbins=f)

    carrier = np.sin(200 * np.pi * t + np.pi)
    PSK = carrier * y
    plt.subplot(212)
    plt.title("Modulation")
    plt.grid(True, linestyle='-.')
    plt.plot(t, PSK, linewidth=1, linestyle="-")  # 绘制
    plt.show()

    timeLine, fft_single, f_single = fft_waveform(PSK, f, N, N)
    drawTheGraph(PSK, timeLine, fft_single, f_single, f * N, "BPSK波形及频谱分析")

    signal_add_whiteNoise1 = PSK + wN.wgn(PSK, 0.1)
    plt.figure(figsize=(10, 14), dpi=80)
    plt.subplot(411)
    plt.title("SNR=1")
    plt.grid(True, linestyle='-.')
    plt.plot(timeLine, signal_add_whiteNoise1, linewidth=1, linestyle="-")  # 绘制

    signal_add_whiteNoise10 = PSK + wN.wgn(PSK, 10)
    plt.subplot(412)
    plt.title("SNR=10")
    plt.grid(True, linestyle='-.')
    plt.plot(timeLine, signal_add_whiteNoise10, linewidth=1, linestyle="-")  # 绘制

    signal_add_whiteNoise20 = PSK + wN.wgn(PSK, 20)
    plt.subplot(413)
    plt.title("SNR=20")
    plt.grid(True, linestyle='-.')
    plt.plot(timeLine, signal_add_whiteNoise20, linewidth=1, linestyle="-")  # 绘制

    signal_add_whiteNoise50 = PSK + wN.wgn(PSK, 50)
    plt.subplot(414)
    plt.title("SNR=50")
    plt.grid(True, linestyle='-.')
    plt.plot(timeLine, signal_add_whiteNoise50, linewidth=1, linestyle="-")  # 绘制
    plt.show()
    yt, t = lpf.bpfDataOnly(1, N * f, 50, 150, signal_add_whiteNoise10)  # t有fs个点，即N*f
    yt = yt * carrier
    y2, t1 = lpf.lpfDataOnly(2, N * f, f, yt)  # t有fs个点，即N*f
    position = int(N / 2)
    y_out = []
    for i in range(N * f):
        y_out.append(0)
    for i in range(f):
        y_out[i * N + position] = 1
    y2 = y_out * y2
    plt.figure()
    plt.title("SNR=10的情况下的解调")
    plt.plot(t, y2)
    plt.show()

    demodulation_y = []
    y_demod = []
    for code in y2:
        if code == 0:
            continue
        elif code < 0:
            y_demod.append(-1)
            for i in range(N):
                demodulation_y.append(-1)
        else:
            y_demod.append(1)
            for i in range(N):
                demodulation_y.append(1)
    plt.figure()
    plt.plot(t, demodulation_y)
    plt.show()


def errorRate():
    eng.errorRate(nargout=0)
    # f = 50
    # N = 2000
    # t = np.linspace(0, f, f * N)  # 时间轴
    # # y = np.ones((f, N), int)
    # # mt = []
    # # for i in range(f):
    # #     r_code = int(round(np.random.random()))
    # #     y[i] = r_code * 2 - 1  # 双极性
    # #     mt.append(r_code * 2 - 1)
    # # y = y.flatten()  # 降维
    # errorrateList = []
    # BPSK_t_AWGN = []
    # carrier = np.sin(200 * np.pi * t + np.pi)
    # y = np.ones((f, N), int)
    # mt = []
    # for i in range(f):
    #     r_code = int(round(np.random.random()))
    #     y[i] = r_code * 2 - 1  # 双极性
    #     mt.append(r_code * 2 - 1)
    # y = y.flatten()  # 降维
    # PSK = carrier * y
    # for SNR in range(-10, 8):
    #     print(SNR)
    #     errorbits = 0
    #     for part in range(2000):
    #
    #         signal_add_whiteNoise = PSK + wN.wgn(PSK, SNR)
    #         yt, t = lpf.bpfDataOnly(1, N * f, 50, 170, signal_add_whiteNoise)  # t有fs个点，即N*f
    #         yt = yt * carrier
    #         y2, t1 = lpf.lpfDataOnly(2, N * f, f, yt)  # t有fs个点，即N*f
    #         position = int(N / 2)
    #         y_out = []
    #         for i in range(N * f):
    #             y_out.append(0)
    #         for i in range(f):
    #             y_out[i * N + position] = 1
    #         y2 = y_out * y2
    #         demodulation_y = []
    #         y_demod = []
    #         for code in y2:
    #             if code == 0:
    #                 continue
    #             elif code < 0:
    #                 y_demod.append(-1)
    #                 for i in range(N):
    #                     demodulation_y.append(-1)
    #             else:
    #                 y_demod.append(1)
    #                 for i in range(N):
    #                     demodulation_y.append(1)
    #         for index in range(len(y_demod)):
    #             if y_demod[index] != mt[index]:
    #                 errorbits += 1
    #     BPSK_t_AWGN.append(0.5 * math.erfc(math.sqrt(10 ** (SNR / 10))))
    #     print(SNR, "dB：", errorbits)
    #     errorrateList.append(errorbits/10000)
    #
    # plt.semilogy(range(-10, 8), errorrateList)
    # plt.semilogy(range(-10, 8), BPSK_t_AWGN)
import squareWave as squW


def RZFunc(isSingle=1):
    """
    Parameters
    ----------
    isSingle: bool
        是单极性，isSingle=1；是双极性，isSingle=0
        默认为1
    """
    if isSingle:
        single = input("请输入一串单极性归零码：")
        title = "单极性归零码"
    else:
        single = input("请输入一串双极性归零码：")
        title = "双极性归零码"
    duty = float(input("输入正占空比："))
    Fs, f = input("输入Fs和f：").split()
    Fs = int(Fs)
    f = int(f)
    wave_single, timeLine, fft_single, f_single = squW.analyse_single(single, duty, Fs, f, isSingle)
    squW.drawTheGraph(wave_single, timeLine, fft_single, f_single, Fs, title)
    return

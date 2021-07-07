import matplotlib

import singleRZFunc
import menuFunc as mf
import conversionAMI as ami
import bpskMod

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 设置字体为微软雅黑，以便输出图像中可以使用中文
q1 = mf.menu1()
if q1 == '1':  # 设计题目1 基带码型仿真
    q1_1 = mf.menu1_1()
    if q1_1 == 1:  # 单双极性归零码
        choice = mf.menu1_1_1()
        singleRZFunc.RZFunc(choice)
    elif q1_1 == 2:  # AMI & HDB3
        number, Fs, f = mf.menu1_1_2()
        # ami.ami_show(number)
        ami.ami_hdb3show(number, Fs, f, 0)
elif q1 == '2':  # 设计题目2 数字带通调制仿真
    bpskMod.BPSK()
elif q1 == '3':
    bpskMod.errorRate()
else:
    print("非法输入")
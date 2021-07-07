def menu1():
    print("------通信原理软件实验------")
    print("设计题目1 基带码型仿真")
    print("设计题目2 数字带通调制仿真")
    print("设计题目3 数字带通调制仿真误码率实验")
    q1 = input("选择题目：")
    return q1


def menu1_1():
    print("------------------------")
    print("设计题目(1) 单双极性归零码的波形及功率谱")
    print("设计题目(2) 随机消息码序列转换为AMI与HDB3及其波形与功率谱")
    q1_1 = int(input("选择题目："))
    return q1_1


def menu1_1_1():
    print("------------------------")
    answer = int(input("单双极性选择;单极性为1，双极性为2："))
    if answer == 1:
        q1_1_1 = True
    elif answer == 2:
        q1_1_1 = False
    else:
        print("input error")
        return
    return q1_1_1


def menu1_1_2():
    print("------------------------")
    answer = int(input("随机消息序列位数："))
    Fs, f = input("输入Fs和f：").split()
    Fs = int(Fs)
    f = int(f)
    return answer, Fs, f

clc
clear
% 产生10^7bit个随机的+1,-1码
N = 10000000;
for i=1:N
    if rand <.5
        s(i)=-1;
    else
        s(i)=1;
    end
end

% 产生高斯白噪声，randn函数产生10^7个正态分布的伪随机数
b=randn(1,N);
% 信噪比
EbNo=[0:1:10];
% 针对以上的情况的11种信噪比加入白噪声
for j = 1:11
        sigma(j) = power(10,(-EbNo(j)/20))/ sqrt (2);
    for i = 1:N
        n(i)=sigma(j)*b(i);
        y(i)=s(i)+n(i); % S（i）是输入的码，n(i)为噪声
    end
    % 解码，demo为解码后的结果
    ER(j) = 0;
    for i=1:N
        if y(i) > 0
            Demo(i) = 1;
        else
            Demo(i) = -1;
        end
        % 统计误码数，算出误码率,BER意为bit error ratio，比特出错概率，TBER意为理论比特出错概率，erfc为单调增函数，计算误码率和信噪比的关系
        if Demo(i) ~= s(i)
            ER(j) = ER(j) + 1;
        end
    end
        BER(j) = ER(j) / N;
        TBER(j) = erfc(sqrt(power(10,EbNo(j)/10)))/2;
end

% semilogy函数可以使用y轴的对数刻度绘制数据
figure
semilogy(EbNo,BER,'B-V',EbNo,TBER,'M-X');
grid on;
legend('仿真误码率曲线','理论误码率曲线');
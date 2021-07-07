function errorRate()
    clear
    clc

    SNR=-4:1:15;
    snr=10.^(SNR/10);
    N=10^7;
    M=2;
    x=randi([0,1],1,N);
    y=pskmod(x,M);

    for i=1:length(SNR)
        N0=1/2/snr(i);
        N0_dB=10*log10(N0);
        ni=wgn(1,N,N0_dB);

        yAn=y+ni;
        yA=pskdemod(yAn,M);
        bit_A=length(find(x~=yA));
        BPSK_s_AWGN(i)=bit_A/N;

    end
    BPSK_t_AWGN=1/2*erfc(sqrt(snr));%AWGN信道下BPSK理论误码率

    %绘制图形
    figure;
    semilogy(SNR,BPSK_s_AWGN,'-bx');hold on;
    semilogy(SNR,BPSK_t_AWGN,'-ro');hold on;
    axis([-5,16,10^-9,1]);
    grid on
    legend('仿真','理论公式');
    title('BPSK误码率曲线');
    xlabel('信噪比（dB）');
    ylabel('误码率');


from scipy import signal
import wave
import numpy as np
import matplotlib.pyplot as plt

def getsignal(wf):
    wf = wave.open("exam.wav", "r")
    frames = wf.getnframes()
    sample_width = wf.getsampwidth()

    fs = wf.getframerate()
    T = 1 / fs
    t = np.arange(0, frames * T, T)
    
    org_signal = wf.readframes(frames)
    org_signal = np.frombuffer(org_signal, dtype="int16") / 2 ** (sample_width * 8 - 1)
    return org_signal, t, fs, frames

def delayFilter(delay_list, org_signal, test_signal, fs, frames, t):
    for delay in delay_list:
        delayfilter = signal.firwin(numtaps=delay, cutoff=fs/4, fs=fs)
        sig = signal.lfilter(delayfilter, 1, test_signal)
        ffted = np.fft.fft(sig)
        amp = np.abs(ffted / (frames / 2))

        plt.plot(t, sig, label="Delayed")
        plt.plot(t, org_signal, label="Original")
        plt.xlim(0.01, 0.02)
        plt.xlabel("time[s]")
        plt.ylabel("frequency[Hz]")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0, fontsize=14)
        plt.show()

# 音声データの読み込み
wf = wave.open("exam.wav", "r")
org_signal, t, fs, frames = getsignal(wf)

test_signal = org_signal

delay_list = [14*1, 14*2, 14*3, 14*4, 14*5, 14*6]
delayFilter(delay_list, org_signal, test_signal, fs, frames, t)

delay_list = [20*1, 20*2, 20*3, 20*4]
delayFilter(delay_list, org_signal, test_signal, fs, frames, t)

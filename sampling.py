from matplotlib.pyplot import subplots, show as show_plots
from numpy import zeros, linspace, array, exp, convolve, dtype, pi, abs
from numpy.fft import fft, fftfreq 
from Nsound import AudioStream, AudioPlayback, Buffer
from wave import open as wav_open


def plot(x, y):
    fig, ax = subplots()
    ax.plot(x, y)
    show_plots(block=False)


def stem(x, y):
    fig, ax = subplots()
    ax.stem(x, y)
    show_plots(block=False)


def indices(x):
    return linspace(0, len(x) - 1, len(x))


def pad(x, n):
    x_p = zeros(len(x) * n)
    for i in range(len(x_p)):
        if i % n == 0:
            x_p[i] = x[int(i / n)]
        else:
            x_p[i] = 0

    return x_p


def decimate(x, n):
    x_d = zeros(int(len(x) / n))
    for i in range(len(x_d)):
        x_d[i] = x[int(10 * i)]

    return x_d


def play(sound_file, w=16):
   a = AudioStream(sound_file)
   p = AudioPlayback(a.getSampleRate(), a.getNChannels, w) 
   a >> p
        

def make_wav(x, file_name, w=16, f=44100):
    width = w / 8 # width in bytes
    wav_file = wav_open(file_name, "wb")
    wav_file.setnchannels(1)
    wav_file.setsampwidth(width)
    wav_file.setframerate(f)
    wav_file.writeframes(x)
    wav_file.close()


def dtft(x, w, p=1000):
    dtft_v = zeros(len(w))

    for n in range(len(x)):
        dtft_v = dtft_v + (x[n] * exp(-1j* w*n))

    return dtft_v


# vim: ai: et: ts=4: sts=4

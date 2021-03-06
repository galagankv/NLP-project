import numpy as np
import pywt
import matplotlib.pyplot as plt
vav = 'cgau5'
wav = pywt.ContinuousWavelet(vav)
# вывести диапазон, в котором будет оцениваться вейвлет
print("Непрерывный вейвлет будет оцениваться во всем диапазоне [{}, {}]".format(wav.lower_bound, wav.upper_bound))
width = wav.upper_bound - wav.lower_bound
scales = [1, 2, 3, 4, 10, 15]
max_len = int(np.max(scales)*width + 1)
t = np.arange(max_len)
fig, axes = plt.subplots(len(scales), 2, figsize=(12, 6))
for n, scale in enumerate(scales):
    # Следующий код адаптирован из внутренних частей cwt
    int_psi, x = pywt.integrate_wavelet(wav, precision=10)
    step = x[1] - x[0]
    j = np.floor(
        np.arange(scale * width + 1) / (scale * step))
    if np.max(j) >= np.size(int_psi):
        j = np.delete(j, np.where((j >= np.size(int_psi)))[0])
    j = j.astype(np.int)
    # normalize int_psi для более простого построения
    int_psi /= np.abs(int_psi).max()
  # дискретные выборки интегрированного вейвлета
    filt = int_psi[j][::-1]
# CWT состоит из свертки фильтра с сигналом в этой шкале
# Здесь мы строим это дискретное ядро свертки в каждом масштабе.
    nt = len(filt)
    t = np.linspace(-nt//2, nt//2, nt)
    axes[n, 0].plot(t, filt.real, t, filt.imag)
    axes[n, 0].set_xlim([-max_len//2, max_len//2])
    axes[n, 0].set_ylim([-1, 1])
    axes[n, 0].text(50, 0.35, 'scale = {}'.format(scale))
    f = np.linspace(-np.pi, np.pi, max_len)
    filt_fft = np.fft.fftshift(np.fft.fft(filt, n=max_len))
    filt_fft /= np.abs(filt_fft).max()
    axes[n, 1].plot(f, np.abs(filt_fft)**2)
    axes[n, 1].set_xlim([-np.pi, np.pi])
    axes[n, 1].set_ylim([0, 1])
    axes[n, 1].set_xticks([-np.pi, 0, np.pi])
    axes[n, 1].set_xticklabels([r'$-\pi$', '0', r'$\pi$'])
    axes[n, 1].grid(True, axis='x')
    axes[n, 1].text(np.pi/2, 0.5, 'scale = {}'.format(scale))
axes[n, 0].set_xlabel('time (samples)')
axes[n, 1].set_xlabel('frequency (radians)')
axes[0, 0].legend(['real', 'imaginary'], loc='upper left')
axes[0, 1].legend(['Power'], loc='upper left')
axes[0, 0].set_title('filter: wavelet - %s'%vav)
axes[0, 1].set_title(r'|FFT(filter)|$^2$')
plt.show()
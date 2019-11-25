import numpy as np
import scipy.signal as ss
import pylab as py

Fs = 100.0
t = np.arange(0,1,1/Fs)

x = np.sin(2*np.pi* 10 *t) #np.random.randn(len(t))
x_ma = np.zeros(len(x))
p = 3
for i in range(len(x)-p):
    x_ma[i+p-1] = np.mean(x[i:i+p])
py.plot(t,x,'b',t,x_ma,'r')
py.show()


##########

f = np.zeros(100)
N = int(len(f)/2.)
f[N-10:N+11 ] =1
x =np.fft.ifft(f)
py.plot(np.abs(np.fft.fftshift(x)))
py.show()
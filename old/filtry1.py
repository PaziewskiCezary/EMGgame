# -*- coding: utf-8 -*-

import numpy as np
import pylab as py
from  scipy.signal import freqz, firwin, cheby2, lfilter
 
 
#b = firwin(5,0.5)# licznik
#a = np.array([1.0]) # mianownik
Fs = 200.0
FN = Fs/2.
t = np.arange(0,2,1./Fs)
b, a =  cheby2(1,10,np.array([49 ,51])/FN,btype = 'bandstop')
#n = 1000 # n ilo?? punkt?w na kt?rych b?dzie obliczona funkcja h
#w, h = freqz(b,a,n) 
#w =w/np.pi *FN 
#m = np.abs(h) # modu? transmitancji
#phi = np.unwrap(np.angle(h)) # faza
#py.subplot(4,1,1)
#py.plot(w,20*np.log10(m))
#py.ylabel('[dB]')
#py.title(u'modu? transmitancji')
#py.subplot(4,1,2)
#py.plot(w,phi)
#py.title(u'faza transmitancji')
#py.ylabel('rad')
#py.xlabel(u'rad/pr?bki')
##fazowe = - phi/w
#py.subplot(4,1,3)
##py.plot(w,fazowe)
#py.ylim([20,30])
#py.title(u'op??nienie fazowe')
#py.ylabel(u'pr?bki')
#py.xlabel('rad')
# 
# 
#grupowe = - np.diff(phi)/np.diff(w)
#py.subplot(4,1,4)
#py.plot(w[:-1],grupowe)
#py.ylim([20,30])
#py.title(u'op??nienie grupowe')
#py.ylabel(u'pr?bki')
#py.xlabel('rad')
# 
#py.show()


x1 = np.sin(2*np.pi*50*t)
x2 = np.sin(2*np.pi*10*t)
x= 30*x1+x2
py.plot(t,x)

y = lfilter(b,a,x)
py.plot(t,y,'r')
py.plot(t,x2,'.')
py.show()

x = np.zeros(len(t))
x[100]=1
y = lfilter(b,a,x)
py.plot(t,y,'r')
py.plot(t,x,'.')
py.show()
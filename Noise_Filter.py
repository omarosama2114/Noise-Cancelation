import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
import random
import math
from scipy.fftpack import fft


samples = 12 * 1024
t = np.linspace(0 , 3 , samples)

leftHand = [130.81,146.83,164.81,174.61,196,220,246.93] #3rd Octave f's
rightHand = [261.63,293.66,329.63,349.23,392,440,493.88] #4th Octave f's

amplitude = [0.5,0.75,1,1.25,1.5]

N = 6

x = np.where(t>=0 , 0 , 0)

TS = 0     #ti
TD = random.uniform(0.1, 0.5)  #Ti

j1 = random.randint(0,6)
j2 = random.randint(0,6)
j3 = random.randint(0,4)

for i in range(N):
    
    FL = leftHand[i]    #Fi
    FR = rightHand[i]   #fi
    
    x1 = np.sin(2*np.pi*FL*t) + np.sin(2*np.pi*FR*t)
    
    x3 = np.where(t-TS>=0 , 1 , 0)
    x4 = np.where(t-TS-TD>=0 , 1 , 0)
    
    x2 = np.subtract(x3, x4)
    
    cur = np.multiply(x1, x2)
    
    x = amplitude[j3] * np.add(x, cur)
    
    TS += 0.5
    TD = random.uniform(0.1, 0.5)
    j1 = random.randint(0,6)
    j2 = random.randint(0,6)
    j3 = random.randint(0,4)

N1 = 3*1024
f = np. linspace(0 , 512 , int(N1/2))

x_f = fft(x)
x_f = 2/N1 * np.abs(x_f [0:np.int(N1/2)])

fn1 = np. random. randint(0, 512, 1)
fn2 = np. random. randint(0, 512, 1)

noise = np.sin(2*np.pi*fn1*t) + np.sin(2*np.pi*fn2*t)

xn = x + noise 

xn_f = fft(xn)
xn_f = 2/N1 * np.abs(xn_f [0:np.int(N1/2)])

maxAmp = math.ceil(max(x_f))

noiseFound = []

for i in range(len(xn_f)):
    if(xn_f[i] > maxAmp):
        noiseFound.append(math.floor(f[i]))
      
x_filtered = xn - (np.sin(2*np.pi*noiseFound[0]*t) + np.sin(2*np.pi*noiseFound[1]*t))
  
x_filtered_f = fft(x_filtered)
x_filtered_f = 2/N1 * np.abs(x_filtered_f [0:np.int(N1/2)]) 
   
sd.play(x_filtered, 3 * 1024)
        
fig, ax = plt.subplots(3)
ax[0].plot(t, x) 
ax[1].plot(t, xn) 
ax[2].plot(t,x_filtered) 
plt.show()

fig, ax1 = plt.subplots(3)
ax1[0].plot(f,x_f)
ax1[1].plot(f,xn_f)
ax1[2].plot(f,x_filtered_f)  
plt.show()
        

        

        
        
    
    
   
     
    
    
    

  
    
    


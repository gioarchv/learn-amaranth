import numpy as np
import matplotlib.pyplot as plt
import math


Fs = 97656.25      # Sampling frequency
f = 1000           # Signal frequency
A = 32767          # Amplitude
norm_f = f / Fs
N = 1 / norm_f     
n = np.arange(N)

y = A * np.sin(2*np.pi*n*norm_f)

table = np.round(y).astype('i2')
print(",".join(map(str, table)))
print('Table size: ', table.size)
print('Datatype: ', table.dtype)

plt.figure(figsize=(10,8))
plt.title(f'Lookup Table - Sinusoid, Fs = {Fs/1000} khz, f = {f/1000} khz, Amplitude = {2*A}')
plt.xlabel("Sample[n]")
plt.ylabel("Amplitude")
plt.stem(table)
plt.grid()
plt.show()
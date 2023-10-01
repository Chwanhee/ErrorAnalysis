import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
A = np.array([[0.0003,0.0005,0.0001,0.0002,0,-0.0002,-0.0001,0.0002],
              [1.0018,0.9982,0.9988,1.0029,1.0001,0.9985,1.0022,1.0066]])
B = np.arange(3.1,5.1,0.1)
C = np.zeros((20,8))
for i in range(len(B)):   #20개 전압
    for j in range(len(A[0])):   #8개 저항
        C[i][j] = A[0][j]*B[i]+A[1][j]
C = np.reciprocal(C)
dd = []
for i in range(len(B)):
    dd.append((len(A[0])+1)*1000/(np.sum(C[i])+1))

reference = np.mean(dd)
x = B
y = dd
print(x)
print(y)

def func(x, A, B):
    return A*x+ B

popt, pcov = curve_fit(func, x, y)
print("params:\n", popt)
print("covariance:\n", pcov)
a, b= popt[0], popt[1]
yfit = a*x+b

fig, ax = plt.subplots()
ax.plot(x,yfit)
ax.plot(x,y)
plt.scatter(x,y)
#plt.xlim((1001.3,1001.6))
plt.xscale('linear')
plt.yscale('linear')
plt.show()
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import pickle

handle = open("series_resistances.pkl",'rb')
A = pickle.load(handle)
handle.close()


volt_in = A.keys() # List of input voltages

n = len(volt_in)      # number of voltage
m = len(A.get(list(A.keys())[0]))       # number of measurement in each voltage

B = {}       # temporary storage
#C = {}
C = []       # [input voltage, V1/V2, 1 sigma error]
for i in range(n):      
    mean = np.mean(A.get(list(A.keys())[i]))      # generate list[mean of V_1, mean of V_2]
    std = np.std(A.get(list(A.keys())[i]), axis = 0, ddof = 1)      # generate list[sample standard deviation of V_1, sample standard deviation of V_2]
    B[list(A.keys())[i]] = [[mean[0], std[0]], [mean[1], std[1]]]       # generate pair input voltage : list[[mean_V1, SSD_V1], [mean_V2, SSD_V2]]
    #C[list(A.keys())[i]] = [mean[0]/mean[1], mean[0]/mean[1]*((std[0]/mean[0])**2+(std[1]/mean[1])**2)**0.5]         # generate pair input voltage : [V_1/V_2, 1 sigma error]
    C.append([list(A.keys())[i], mean[0]/mean[1], mean[0]/mean[1]*((std[0]/mean[0])**2+(std[1]/mean[1])**2)**0.5])

D = np.array(C).T
print(D)
x = D[0]
y = D[1]
stdv = D[2]

def func(x, A, B):
    return A+ x*B

popt, pcov = curve_fit(func, x, y)
print("params:\n", popt)
print("covariance:\n", pcov)
a, b= popt[0], popt[1]
yfit = a*x+b
max = list(A.keys())[-1]
fig, ax = plt.subplots()
ax.plot(x, func(x, a, b),
    linestyle="-",
    linewidth=1.2,
    color="k",
    label=r"Fitted graph for $\frac{V_1}{V_2}$")
ax.errorbar(x, y, yerr=stdv,
    marker='o',
    markersize=4,
    linestyle="None",
    elinewidth=1.2,
    capsize=1.5,
    capthick=1.2,
    color="r",
    label="Data point")

plt.rc('text', usetex = True)
#plt.xkcd()
plt.title(r'ratio of applied voltage $\frac{V_1}{V_2}$', fontsize = 20)

plt.ylabel(r'$\frac{V_1}{V_2}$', fontsize = 20)
plt.xlabel(r'applied voltage [$V$]', fontsize = 20)
plt.legend(loc='best', fancybox=True, shadow=True)
plt.grid(False)
plt.show()

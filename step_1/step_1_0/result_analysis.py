import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
'''
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
'''
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib
import pickle
res1 = 1001.44
res2 = [1000.1,1000.2,1000.3,1000.4,1000.5,1000.6,1000.7,1000.8]
parameters = []
color1=0
fig, ax = plt.subplots()
def func(x, A, B):
    return A*x+ B
for ohm in res2:
    with open("step1_ex1_res_"+str(ohm)+'.pkl',"rb") as handle:
        A = pickle.load(handle)
#print(A)
    n = len(A)      # number of voltage
    m = len(A.get(list(A.keys())[0]))       # number of measurement in each voltage
#print(n,m)
    B = {}       # temporary storage
    C = []       # [input voltage, V1/V2, 1 sigma error]
    for i in range(n):      
        mean = np.mean(A.get(list(A.keys())[i]), axis = 0)      # generate list[mean of V_1, mean of V_2]
        std = np.var(A.get(list(A.keys())[i]), axis = 0, ddof = 1)/(m**0.5)      # generate list[sample standard deviation of V_1, sample standard deviation of V_2]
        B[list(A.keys())[i]] = [[mean[0], std[0]], [mean[1], std[1]]]       # generate pair input voltage : list[[mean_V1, SSD_V1], [mean_V2, SSD_V2]]
        #C[list(A.keys())[i]] = [mean[0]/mean[1], mean[0]/mean[1]*((std[0]/mean[0])**2+(std[1]/mean[1])**2)**0.5]         # generate pair input voltage : [V_1/V_2, 1 sigma error]
        C.append([list(A.keys())[i], mean[0]/mean[1], mean[0]/mean[1]*((std[0]/mean[0])**2+(std[1]/mean[1])**2)**0.5])
#print(C)
    D = np.array(C).T
#print(D)
    x = D[0]
    y = D[1]
    stdv = D[2]
    popt, pcov = curve_fit(func, x, y)
    parameters.append([ohm, round(popt[0], 4), round(pcov[0][0]**0.5, 4), round(popt[1], 4), round(pcov[1][1]**0.5)])
    #print('DUT is '+str(ohm))
    #print("params:\n", popt)
    #print("covariance:\n", pcov)
    print('y=ax+b for DUT '+str(ohm)+','+'\na='+str(round(popt[0], 4))+'±'+str(round(pcov[0][0]**0.5, 4))+'\nb='+str(round(popt[1], 4))+'±'+str(round(pcov[1][1]**0.5, 4)))
    a, b= popt[0], popt[1]
    yfit = a*x+b
    max = list(A.keys())[-1]
    color2='C'+str(color1)
    ax.plot(x, func(x, a, b),
        linestyle="-",
        linewidth=1.2,
        color=color2,
        label="Fitted graph for "+ str(ohm) +r"$\Omega$")

    ax.errorbar(x, y, yerr=stdv,
        marker='o',
        markersize=4,
        linestyle="None",
        elinewidth=1.2,
        capsize=1.5,
        capthick=1.2,
        color=color2)
        #label="Data point for"+ str(ohm) +r"$\Omega$")
    color1+=1
#textstr = 'Reference resistor: '+str(res1)+'\nDUT: '+str(res2)+'\nFitting function: y=ax+b'+'\na='+str(round(popt[0], 4))+r'$\pm$'+str(round(pcov[0][0]**0.5, 4))+'\nb='+str(round(popt[1], 4))+r'$\pm$'+str(round(pcov[1][1]**0.5, 4))
#textbox = matplotlib.offsetbox.AnchoredText(textstr, loc='upper right')
#ax.add_artist(textbox)

plt.rc('text', usetex = True)
#plt.xkcd()
plt.title(r'ratio of applied voltage $\frac{\mathrm{DUT}}{\mathrm{Reference}}$', fontsize = 20)

plt.ylabel(r'$\frac{\mathrm{DUT}}{\mathrm{Reference}}$', fontsize = 20)
plt.xlabel(r'applied voltage [$V$]', fontsize = 20)
plt.legend(loc='lower right', fancybox=True, shadow=True)
plt.grid(False)
plt.savefig('step1_1.png')
plt.show()
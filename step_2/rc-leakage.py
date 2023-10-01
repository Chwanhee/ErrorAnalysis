# Code designed to measure the leakage current from an RC curve. 

import numpy as np
import matplotlib.pyplot as plt

from tqdm import tqdm
import pickle

import swimAD2 as ad2
import time

####### End of importing #######

def sampling(time):
    hertz = 100e6
    size = time*hertz 
    if size <= 8192:
        return size,hertz
    else: 
        size = 8192
        hertz = size/time
        return size,hertz
    
def config_measurement(tinterval,volt):
    # Set the oscilloscope rate to measure for tinterval.
    size,rate = sampling(tinterval)
    # Set the gain of the oscilloscope (high or low).
    rng = 1 if volt<5 else 25 
    ad2.config_oscilloscope(zoroku,
        range0=rng,
        range1=rng,
        sample_rate = rate,
        sample_size= size,
        )
### End of function defining ###


##### Start of actual code #####
ad2.disconnect()
zoroku = ad2.connect(0)

print("Make sure the components' values were correctly input.")

# Measurements of the components. 
Res = [150,220,330,470,510] # Resistances in Ohms.
Cap = 10e-6 # Capacitance in Fahrads. 
    
# "Threshold" is the fraction of capacitor left to full charge
# It can't be smaller than leakage (orders of uA).

threshold = 1e-4 # Fraction of capacitor left to full charge. 

tau = Res[0]*Cap
t_wait = -tau*np.log(threshold) # Expected time to charge. 
discharge = t_wait*10

print("%5f s to charge, %5f s to discharge" % (t_wait,discharge))

volt_in = [.1,.5,
           1,1.5,
           2,2.5,
           3,3.5,
           4,4.5,
           5
           ] # LIST of voltages to try.  
n_trial = range(5) # LIST of trials per voltage.

data_dict = {"cap": Cap,"res": Res,
            "thresh":threshold
            }
for i,R in enumerate(Res): 
    data_dict[R] = {}
    for volt in volt_in: 
        data_dict[R][volt] = {}
        for trial in n_trial:
            trial = str(trial+1)+"th"
            data_dict[R][volt][trial] = {"rise": "Charging",
                                    "fall":"Leakage"
                                    }

for R in Res:
    downtime = len(volt_in)*60*len(n_trial)*(t_wait+5+discharge)/60
    print("Expected wait time : %2f min" % downtime)
    for volt in tqdm(volt_in):
        for trial in data_dict[R][volt].keys():
            ad2.config_wavegen(zoroku, 
                            frequency=0,
                            amplitude=0,
                            offset=volt
                            )
            config_measurement(t_wait,volt)
            ad2.start_wavegen(zoroku,channel=0)

            data_dict[R][volt][trial]["rise"] = ad2.measure_oscilloscope(zoroku)
            
            config_measurement(5,volt)
            t,v0,v1 = ad2.measure_oscilloscope(zoroku)
            t += t_wait

            data_dict[R][volt][trial]["fall"] =  t,v0,v1

            ad2.stop_wavegen(zoroku,channel=0)
            ad2.reset_wavegen(zoroku,channel=0)

            # We let the system discharge
            time.sleep(discharge)
        time.sleep(60)
    handle = open("Error_Analysis\\step_2\\rc-leakage.pkl", 'wb')
    pickle.dump(data_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
    handle.close()

    print("Data up to resistor %d has been collected and saved." % R)
    input("Switch resistor, then press ENTER to measure.")
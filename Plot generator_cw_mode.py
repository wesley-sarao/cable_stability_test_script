# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 15:39:30 2025

@author: wnewton
"""

import numpy as np
import pyvisa
import time
from numpy import double
import os
from datetime import datetime
import matplotlib.pyplot as plt





initial_file_name = 'measurements//Withwave W102-NM1SM1-2M stability test 5'


S21_mag = np.load(initial_file_name +' %s.npy' % 'S21_mag(dB)')

#%%
S21_ph = np.load(initial_file_name +' %s.npy' % 'S21_phase')

#%%
S43_mag = np.load(initial_file_name +' %s.npy' % 'S43_mag(dB)')
S43_ph = np.load(initial_file_name +' %s.npy' % 'S43_phase')

#%%

plt.figure(1)
plt.clf()

plt.plot(S43_ph[0, 1:],
         S43_ph[3, 1:],
         linewidth=1,

         label='S43_phase')


# plt.plot(data3[1:, 0],
#          data3[1:, 181],
#          linewidth=1,

#          label='S43')
# plt.plot(p_out_cold_dBm[0, data_s:data_f],
#          p_out_cold_dBm[1, data_s:data_f],
#          linewidth=1,
#          color='b',
#          label='Pout (cold load)')
plt.legend(loc='upper right')
plt.title("Title")
plt.xlabel("freq")
plt.ylabel("S")
plt.grid(which='both',
         color='black',
         linestyle='-',
         linewidth=0.5)
#plt.ylim((-120,-20))
#plt.xlim((f_start, f_stop))
fig = plt.gcf()
fig.set_size_inches(8, 6, forward=True)
    # fig.savefig(working_file_name + ' powers.png', dpi=200)
    

#%%

plt.figure(2)
plt.clf()

# Parameters and indices

# Calculate phase stability and convert to ppm

# Create the primary axis
fig, ax1 = plt.subplots()

# Plot DUT corrected phase stability
# ax1.plot(S21_ph[1:, 0],
#          (S21_ph[1, 3] - S21_ph[1:, 3])- (S43_ph[1, 3] - S43_ph[1:, 3]),
#          linewidth=1,
#          label='DUT')

# ax1.plot((S21_ph[trim_s, 0],S21_ph[trim_f, 0]),(10,10))

# Plot DUT uncorrected phase stability
ax1.plot(S21_ph[1:, 0],
         (S21_ph[1, 3] - S21_ph[1:, 3]), #- (S43_ph[1, 3] - S43_ph[1:, 3]),
         linewidth=1,
         label='DUT uncorrected')

ax1.plot(S21_ph[1:, 0],
         (S21_ph[1, 3] - S21_ph[1:, 3]) - (S43_ph[1, 3] - S43_ph[1:, 3]),
         linewidth=1,
         label='DUT corrected')

# Plot reference phase stability
ax1.plot(S43_ph[1:, 0],
         S43_ph[1, 3] - S43_ph[1:, 3],
         linewidth=1,
         label='Reference')

# Configure primary axis appearance
ax1.set_xlabel("Time")
ax1.set_ylabel("Phase (degrees)")
ax1.grid(which='both', color='black', linestyle='-', linewidth=0.5)
ax1.legend(loc='upper right')
ax1.set_title("Phase Stability and Temperature Variations")

# Create a secondary y-axis for temperature
ax2 = ax1.twinx()
ax2.plot(S21_ph[1:, 0],
         S21_ph[1:, 1],
         color='red',
         linewidth=1,
         label='Temperature')

ax2.plot(S21_ph[1:, 0],
         S21_ph[1:, 2],
         color='red',
         linewidth=1,
         label='Temperature')

ax2.set_ylabel("Temperature (°C)", color='red')
ax2.tick_params(axis='y', labelcolor='red')

# Adjust figure size
fig.set_size_inches(8, 6, forward=True)

# Optional: Save the figure
# fig.savefig('phase_stability_with_temperature.png', dpi=200)

plt.show()
#%%
plt.figure(3)
plt.clf()


# index = 153
# phase_stability = np.zeros(((len(S21_ph[1:,0])+1)))
# phase_stability_ppm = np.zeros(((len(S21_ph[1:,0]))+1))
# phase_change_ppm = np.zeros(((len(S21_ph[1:,0]))+1))

# for i in range(1,len(S21_ph[1:,0])):
#     delta_phase = S21_ph[1, index]-S21_ph[i, index]  # Normalise to initial value
#     delta_temp = S21_ph[1, 1] - S21_ph[i, 1]  # Normalised to initial temperature
#     # print(i)
#     phase_stability[i] = delta_phase / delta_temp
#     phase_stability_ppm[i] =  (phase_stability[i-1] / 360) * 1e6  # Convert to ppm
#     phase_change_ppm[i] = (delta_phase / 360)* 1e6

# plt.plot(S21_ph[5:, 1],
#          phase_stability_ppm[5:],
#          linewidth=1,
#          label='DUT phase stability ppm')

# # #              # label='S21_phase @ 15.4 GHz')
# plt.plot(S21_ph[1:, 0],
#          S21_ph[1:, index],
#          linewidth=1,
#          label='DUT')

plt.plot(S21_ph[1:, 1],
         (S21_ph[1, 3]-S21_ph[1:, 3])-(S43_ph[1, 3]-S43_ph[1:, 3]),
         linewidth=1,
         label='DUT corrected')

# plt.plot(S21_ph[1:trim_s, 1],
#          (S21_ph[1, index]-S21_ph[1:trim_s, index])-(S43_ph[1, index]-S43_ph[1:trim_s, index]),
#          linewidth=1,
#          label='DUT corrected trimmed')

# plt.plot(S21_ph[trim_f:, 1],
#          (S21_ph[1, index]-S21_ph[trim_f:, index])-(S43_ph[1, index]-S43_ph[trim_f:, index]),
#          linewidth=1,
#          label='DUT corrected trimmed2')


plt.plot(S43_ph[1:, 1],
         S43_ph[1, 3]-S43_ph[1:, 3],
         linewidth=1,
         label='reference')


# plt.plot(S21_ph[1:, 1],
#          (phase_change_ppm[1:]),
#          linewidth=1,
#          label='Phase Change PPM')



plt.legend(loc='upper right')
plt.title("Title")
plt.xlabel("Temperature")
plt.ylabel("Phase")
plt.grid(which='both',
         color='black',
         linestyle='-',
         linewidth=0.5)
# plt.ylim((-25,+25))
# plt.xlim((20, -10))
fig = plt.gcf()
fig.set_size_inches(8, 6, forward=True)
    # fig.savefig(working_file_name + ' powers.png', dpi=200)
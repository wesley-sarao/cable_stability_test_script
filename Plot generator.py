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





initial_file_name = 'measurements//Withwave W102-NM1SM1-2M stability test 3'

S11_mag = np.load(initial_file_name +' %s.npy' % 'S11_mag(dB)')
S21_mag = np.load(initial_file_name +' %s.npy' % 'S21_mag(dB)')
S12_mag = np.load(initial_file_name +' %s.npy' % 'S12_mag(dB)')
S22_mag = np.load(initial_file_name +' %s.npy' % 'S22_mag(dB)')

S21_ph = np.load(initial_file_name +' %s.npy' % 'S21_phase')

S33_mag = np.load(initial_file_name +' %s.npy' % 'S33_mag(dB)')
S43_mag = np.load(initial_file_name +' %s.npy' % 'S43_mag(dB)')
S34_mag = np.load(initial_file_name +' %s.npy' % 'S34_mag(dB)')
S44_mag = np.load(initial_file_name +' %s.npy' % 'S44_mag(dB)')

S43_ph = np.load(initial_file_name +' %s.npy' % 'S43_phase')




# data3 = np.load(initial_file_name +' 2 %s.npy' % 'S43_phase')
# data4 = np.load(initial_file_name +' 2 %s.npy' % 'S43_mag(dB)')

# for value in measurement_list:
#     np.save(working_log_file +' %s.npy' % value, header)

#Frequency data: print(data[0,2:]) print(data[0,181]) - 181 is 18 GHz
# Temperature data: print(data[1:,1])
# Time data: print(data[1:,0])
# recorded data for 18 GHz: print(data[1:,181])

 

plt.figure(1)
plt.clf()
plt.plot(S11_mag[0, 2:],
         S11_mag[1, 2:],
         linewidth=1,

         label='S11_mag')

plt.plot(S21_mag[0, 2:],
         S21_mag[1, 2:],
         linewidth=1,

         label='S21_mag')

plt.plot(S12_mag[0, 2:],
         S12_mag[1, 2:],
         linewidth=1,

         label='S12_mag')

plt.plot(S22_mag[0, 2:],
         S22_mag[1, 2:],
         linewidth=1,

         label='S22_mag')


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
    
    
plt.figure(2)
plt.clf()

plt.plot(S21_ph[0, 2:],
         S21_ph[1, 2:],
         linewidth=1,

         label='S21_phase')



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



plt.figure(3)
plt.clf()
plt.plot(S33_mag[0, 2:],
         S33_mag[1, 2:],
         linewidth=1,

         label='S33_mag')

plt.plot(S43_mag[0, 2:],
         S43_mag[1, 2:],
         linewidth=1,

         label='S43_mag')

plt.plot(S34_mag[0, 2:],
         S34_mag[1, 2:],
         linewidth=1,

         label='S34_mag')

plt.plot(S44_mag[0, 2:],
         S44_mag[1, 2:],
         linewidth=1,

         label='S44_mag')


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
 
plt.figure(4)
plt.clf()

plt.plot(S43_ph[0, 2:],
         S43_ph[1, 2:],
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
    
    
    
plt.figure(5)
plt.clf()

# Parameters and indices
index = 81  # Index of interest for the phase data
trim_s = 2700
trim_f = 3300
n_points = len(S21_ph[1:, 0])  # Number of data points
phase_stability = np.zeros(n_points + 1)  # Initialize phase stability array
phase_stability_ppm = np.zeros(n_points + 1)  # Initialize phase stability in ppm

# Calculate phase stability and convert to ppm
for i in range(1, n_points):
    delta_phase = S21_ph[1, index] - S21_ph[i, index]  # Normalized phase difference
    delta_temp = S21_ph[1, 1] - S21_ph[i, 1]  # Normalized temperature difference
    phase_stability[i] = delta_phase / delta_temp
    phase_stability_ppm[i] = (phase_stability[i - 1] / 360) * 1e6  # Convert to ppm

# Create the primary axis
fig, ax1 = plt.subplots()

# Plot DUT corrected phase stability
ax1.plot(S21_ph[1:, 0],
         (S21_ph[1, index] - S21_ph[1:, index]) - (S43_ph[1, index] - S43_ph[1:, index]),
         linewidth=1,
         label='DUT corrected')

ax1.plot((S21_ph[trim_s, 0],S21_ph[trim_f, 0]),(10,10))

# # Plot DUT uncorrected phase stability
# ax1.plot(S21_ph[1:, 0],
#          (S21_ph[1, index] - S21_ph[1:, index]),
#          linewidth=1,
#          label='DUT uncorrected')

# Plot reference phase stability
ax1.plot(S43_ph[1:, 0],
         S43_ph[1, index] - S43_ph[1:, index],
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
ax2.set_ylabel("Temperature (°C)", color='red')
ax2.tick_params(axis='y', labelcolor='red')

# Adjust figure size
fig.set_size_inches(8, 6, forward=True)

# Optional: Save the figure
# fig.savefig('phase_stability_with_temperature.png', dpi=200)

plt.show()
    
    
plt.figure(6)
plt.clf()


# index = 153

# #              # label='S21_phase @ 15.4 GHz')
plt.plot(S21_mag[1:, 0],
         S21_mag[1, index] - S21_mag[1:, index],
         linewidth=1,
         label='DUT')

plt.plot(S43_mag[1:, 0],
         S43_mag[1, index] - S43_mag[1:, index],
         linewidth=1,
         label='reference')





plt.legend(loc='upper right')
plt.title("Title")
plt.xlabel("Time")
plt.ylabel("S21_mag")
plt.grid(which='both',
         color='black',
         linestyle='-',
         linewidth=0.5)
# plt.ylim((-25,+25))
#plt.xlim((f_start, f_stop))
fig = plt.gcf()
fig.set_size_inches(8, 6, forward=True)
    # fig.savefig(working_file_name + ' powers.png', dpi=200)
    
    
plt.figure(7)
plt.clf()


# index = 153
phase_stability = np.zeros(((len(S21_ph[1:,0])+1)))
phase_stability_ppm = np.zeros(((len(S21_ph[1:,0]))+1))
phase_change_ppm = np.zeros(((len(S21_ph[1:,0]))+1))

for i in range(1,len(S21_ph[1:,0])):
    delta_phase = S21_ph[1, index]-S21_ph[i, index]  # Normalise to initial value
    delta_temp = S21_ph[1, 1] - S21_ph[i, 1]  # Normalised to initial temperature
    # print(i)
    phase_stability[i] = delta_phase / delta_temp
    phase_stability_ppm[i] =  (phase_stability[i-1] / 360) * 1e6  # Convert to ppm
    phase_change_ppm[i] = (delta_phase / 360)* 1e6

# plt.plot(S21_ph[5:, 1],
#          phase_stability_ppm[5:],
#          linewidth=1,
#          label='DUT phase stability ppm')

# # #              # label='S21_phase @ 15.4 GHz')
# plt.plot(S21_ph[1:, 0],
#          S21_ph[1:, index],
#          linewidth=1,
#          label='DUT')

# plt.plot(S21_ph[1:, 1],
#          (S21_ph[1, index]-S21_ph[1:, index])-(S43_ph[1, index]-S43_ph[1:, index]),
#          linewidth=1,
#          # label='DUT corrected')

plt.plot(S21_ph[1:trim_s, 1],
         (S21_ph[1, index]-S21_ph[1:trim_s, index])-(S43_ph[1, index]-S43_ph[1:trim_s, index]),
         linewidth=1,
         label='DUT corrected trimmed')

plt.plot(S21_ph[trim_f:, 1],
         (S21_ph[1, index]-S21_ph[trim_f:, index])-(S43_ph[1, index]-S43_ph[trim_f:, index]),
         linewidth=1,
         label='DUT corrected trimmed2')


plt.plot(S43_ph[1:trim_s, 1],
         S43_ph[1, index]-S43_ph[1:trim_s, index],
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
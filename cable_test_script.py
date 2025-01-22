# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 14:19:14 2025

@author: wnewton
"""

# %% Import functions that do the work
import numpy as np
import pyvisa
import time
from numpy import double
import os
from datetime import datetime
# import matplotlib.pyplot as plt
# import h5py
# import json
# import scipy
# %% Global constants and variable definitions
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
chamber_IP_address = "10.8.88.121"  # IP address of the environmental chamber
chamber_port = "888"  # Environmental application port number
chamber_termination = "\r\n"  # <CR><LF>
vna_IP_address = "10.8.88.130"  # IP address of the vna
vna_port = "5025"  # VNA application port number
vna_termination = "\n"

# %% Metadata for the test
metadata = {
    "measurement_title" : "stability test 3",
    "cable_under_test_manufacturer": "Withwave",
    "cable_under_test_model_number": "W102-NM1SM1-2M",
    "cable_under_test_serial_number": "N/A",
    "cable_under_test_length": "2m",
    "cable_under_test_connector_a": "SMA-m",
    "cable_under_test_connector_b": "N-Type-m",
    "cable_under_test_vna_ports": "Port 1 and Port 2",
    "reference_measurement_description": "Withwave W102-NM1SM1-2M connected between port 3 and port 4 outside the chamber",
    "cable_under_test_additional_adaptor_port_1": "SMA f-f",  # external to the calibration
    "cable_under_test_additional_adaptor_port_2": "SMA f - N-Type f",
    "test_location": "Liesbeek house Receiver Lab",
    "temperature profile" : "25 C to +50 C at 2 degrees per 10 mins (0.20). Soak for 20 min at 50 C, ramp from 50 C to -10 C at 2 degrees in 10 mins (0.20). Soak at -10 for 20 min. Ramp back to 50C at 0.20, soak for 20 mins at 50 C and ramp back down to 25 C at 0.2",
    "calibration_description": '''Channel 1: Two port calibration port 1, port 2 and two port calibration port 3, port 4''',
    "frequency reference": "External - GPS disciplined rubudium clock"
    }



initial_file_name = 'measurements//'+metadata["cable_under_test_manufacturer"]+ ' ' + metadata["cable_under_test_model_number"] + ' ' + metadata["measurement_title"]


# %%
measurement_list = ['S11_mag(dB)',
                    'S21_mag(dB)',
                    'S12_mag(dB)',
                    'S22_mag(dB)',
                    'S21_phase',
                    'S33_mag(dB)',
                    'S43_mag(dB)',
                    'S34_mag(dB)',
                    'S44_mag(dB)',
                    'S43_phase']


# %%
f_points = 201  # number of points in the frequency sweep
f_start = '0.1 GHZ'
f_stop = '20.1 GHZ'
# this will give allow the points to align with GHz designations

# %% Functions
# -----------------------------------------------------------------------------


def initialise_log_file(file_name):
    """Initialise a new log file, iterate the file name if one already exists.

    Args:
        log_file_name (string): The path and filename.

    Returns
    -------
        new_log_file_name (string): The path and filename
        append (bool): Whether or not the file already existed
        i (int): The iteration number to append to the filename

    Note:
 

    Example:
        log_file, file_exists, file_append_nr =
        initialise_log_file(band+'/'+band+'_'+meas)
    """
    # log_file_name = file_name + ' log'
    new_file_name = file_name  # initially they will be the same
    # Only create a new log file if it does not exist
    # check to see if the log file already exists
    i = 1
    while os.path.exists(new_file_name+' log' + '.txt'):
        new_file_name = file_name+' '+str(i)
        print('file exists trying this name:\n %s' %
              (new_file_name+' log' + '.txt'))
        i += 1
        # append = True

    print('new log file created %s' % new_file_name+' log' + '.txt')
    # open the log file with write privelages
    with open(new_file_name+' log' + '.txt', 'w') as log_file:
        log_file.write('Start date and time:' +
                       (datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
        for key in metadata:
            log_file.write(key+':'+metadata[key]+'\n')
        log_file.write('%s \t %s \n' % (
            datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'Logging started'))
    return new_file_name
# %%


def write_to_log_file(local_file_name, contents):
    """Append data to an existing log file.

    Args:
        file_name (string): The path and filename.
        contents (string): The data to append to the file.

    Returns
    -------
        Nothing

    Note:
        The function assumes that the global variables are available:


    Example:
        write_to_log_file(file_name, 'hot measurement started')
    """
    # open the log file with append privelages
    with open(local_file_name+' log' + '.txt', 'a') as log_file:
        log_file.write('%s \t %s \n' % (
            datetime.now().strftime("%d/%m/%Y %H:%M:%S"), contents))

    return

# %% Open socket connection to VNA

def initialise_vna():
    # test at only a few frequency points-be careful of phase across frequency
    vna.write('*RST')  # Reset the instrument
    vna.write('*CLS')  # clear the screen
    # Create a second trace in channel 1, assign the format Phase,
    # and display the new trace in the same diagram area.

    # Channel 1 setup
    vna.write('CONF:CHAN1:STAT ON')  # Create Ch1 and enable
    vna.write('SWEep:TYPE LIN')  # Set up frequency sweep
    vna.write('SENSE1:SWEEP:POINTS %s' % f_points)
    vna.write('FREQ:START %s' % f_start)
    vna.write('FREQ:STOP %s' % f_stop)
    vna.write('SOUR:POW -20')  # Set an appropriate power level for this cable

    # Channel 2 setup
    # vna.write('CONF:CHAN2:STAT ON')  # Create Ch2 and enable
    # vna.write('SWEep:TYPE LIN')  # Set up frequency sweep
    # vna.write('SENSE1:SWEEP:POINTS %s' % f_points)
    # vna.write('FREQ:START %s' % f_start)
    # vna.write('FREQ:STOP %s' % f_stop)
    # set an appropriate power level for this cable
    vna.write('SOUR:POW -20')

    # create four windows
    vna.write('CALCulate:PARameter:DELete:ALL')
    vna.write('DISP:WIND1:STAT ON')
    vna.write('DISP:WIND2:STAT ON')
    vna.write('DISP:WIND3:STAT ON')
    vna.write('DISP:WIND4:STAT ON')


    # Set up traces for Channel 1 window 1 (magnitudes)
    vna.write('CALC1:PAR:SDEF "Ch1_Trc1", "S11" ')
    vna.write('DISP:WIND1:TRAC1:FEED "Ch1_Trc1"')
    vna.write('CALC1:FORM MLOG')
    vna.write('CALC1:PAR:SDEF "Ch1_Trc2", "S21" ')
    vna.write('DISP:WIND1:TRAC2:FEED "Ch1_Trc2"')
    vna.write('CALC1:FORM MLOG')
    vna.write('CALC1:PAR:SDEF "Ch1_Trc3", "S12" ')
    vna.write('DISP:WIND1:TRAC3:FEED "Ch1_Trc3"')
    vna.write('CALC1:FORM MLOG')
    vna.write('CALC1:PAR:SDEF "Ch1_Trc4", "S22" ')
    vna.write('DISP:WIND1:TRAC4:FEED "Ch1_Trc4"')
    vna.write('CALC1:FORM MLOG')


    vna.write('CALC1:PAR:SDEF "Ch1_Trc5", "S21" ')
    vna.write('DISP:WIND3:TRAC1:FEED "Ch1_Trc5"')
    vna.write('CALC1:FORM UPHASE')


    vna.write('CALC1:PAR:SDEF "Ch1_Trc6", "S33" ')
    vna.write('DISP:WIND2:TRAC1:FEED "Ch1_Trc6"')
    vna.write('CALC1:FORM MLOG')
    vna.write('CALC1:PAR:SDEF "Ch1_Trc7", "S43" ')
    vna.write('DISP:WIND2:TRAC2:FEED "Ch1_Trc7"')
    vna.write('CALC1:FORM MLOG')
    vna.write('CALC1:PAR:SDEF "Ch1_Trc8", "S34" ')
    vna.write('DISP:WIND2:TRAC3:FEED "Ch1_Trc8"')
    vna.write('CALC1:FORM MLOG')
    vna.write('CALC1:PAR:SDEF "Ch1_Trc9", "S44" ')
    vna.write('DISP:WIND2:TRAC4:FEED "Ch1_Trc9"')
    vna.write('CALC1:FORM MLOG')


    vna.write('CALC1:PAR:SDEF "Ch1_Trc10", "S43" ')
    vna.write('DISP:WIND4:TRAC1:FEED "Ch1_Trc10"')
    vna.write('CALC1:FORM UPHASE')
    return
# %%

def cal_check():
    # input('please carry out 2 port calibration on CH1 P1-P2 and on CH2 P3-P4')

    # Confirm that the system is calibrated
    vna.write('SYSTEM:DISPLAY:UPDATE:ON')

    write_to_log_file(working_log_file, ('Calibration channel 1:'+vna.query('SENSe1:CORRection:SSTate?')))
    write_to_log_file(working_log_file, ('Calibration date channel 1:'+vna.query('SENSe1:CORRection:DATE?')))
    # write_to_log_file(working_log_file, ('Channel 2:'+vna.query('SENSe2:CORRection:SSTate?')))
    # TODO Can we save the calibration for later?
    return

# %% Initiate the sweep and save the data

def capture_vna_data():

    vna.write('INIT1:CONT OFF')  # Switch to single sweep on channel 1
    # vna.write('INIT2:CONT OFF')  # switch to single sweep on channel 2
    # Carry out the sweep
    # initiate the sweep in channel 1 and wait for confirmation
    vna.write('INIT1:IMM;*WAI')
    # initiate the sweep in channel 1 and wait for confirmation
    # vna.write('INIT2:IMM;*WAI')

    # Fetch the data
    VNA_measurement = {}
    # Query all traces from Channel 1
    trace_array_1 = vna.query('CALC1:DATA:ALL? FDAT')
    # Convert to a numpy array
    trace_1 = np.fromstring(trace_array_1, sep=",")




    # Define the number of traces (adjust this if needed)
    num_traces = len(measurement_list) # Update according to your VNA setup
    num_points = len(trace_1) // num_traces  # Points per trace

    # Reshape into 2D array: (num_traces, num_points)
    trace_1 = trace_1.reshape((num_traces, num_points))

    # It seems like the data is identical whether captured from channel 1 or 2.
    # It is good to seperate them out

    # Copy the data from the measurement list to the VNA_measurement dict

    for value in measurement_list:
            VNA_measurement[value] = trace_1[measurement_list.index(value), :]

    return VNA_measurement

def get_temp_no_check():
    response = tc.query('?tcuve')
    prefix, value = response.split('=')
    return float(value)

def get_temperature(prev_value, max_retries=5, delay=1, threshold=5):
    """
    Queries the device for a temperature value and retries if the response is invalid 
    or if it differs too much from the previous value.

    Parameters:
    - query_function: Function to query the device (e.g., tc.query)
    - prev_value: Previous valid temperature value (float)
    - max_retries: Maximum number of retries for getting valid data
    - delay: Delay (in seconds) between retries
    - threshold: Maximum allowed difference from the previous value

    Returns:
    - A valid temperature value (float) or None if maximum retries are exceeded
    """
    for attempt in range(max_retries):
        response = tc.query('?tcuve')
        try:
            # Parse the response and convert to float
            prefix, value = response.split('=')
            temperature = float(value)
                # Check if the new value differs too much from the previous value
            if prev_value is not None and abs(temperature - prev_value) > threshold:
               print(f"Anomalous temperature detected: {temperature} (diff: {abs(temperature - prev_value)})")
            else:
                return temperature
        except (ValueError, AttributeError) as e:
            print(f"Error parsing response: {response}, Error: {e}")
        
        print(f"Retrying... ({attempt + 1}/{max_retries})")
        time.sleep(delay)
    
    print("Failed to get valid data after maximum retries.")
    return None

def get_time_remaining():
    try:
        response = tc.query('?TpsTot_Restant')
        prefix, value = response.split('=')
        return float(value)/60/60
    except:
        print('error reading remaining time')
        return ''

#%% Main loop

working_log_file = initialise_log_file(initial_file_name)

try:

    # -----------------------------------------------------------------------------
    # Initialise PYVISA resource manager
    rm = pyvisa.ResourceManager()
    # Open socket connection to the environmental chamber
    tc = rm.open_resource(f'TCPIP0::{chamber_IP_address}::{chamber_port}::SOCKET',
                          write_termination=chamber_termination,
                          read_termination=chamber_termination)

    # Test the connection by querying current loaded program
    # print(tc.query("?Programme en cours"))
    chamber_temp = get_temp_no_check()
  
    # Open the vna
    # vna = pyvisa.ResourceManager()

    vna = rm.open_resource("TCPIP0::%s::%s::SOCKET" % (vna_IP_address,
                                                       vna_port),
                           write_termination=vna_termination,
                           read_termination=vna_termination)

    print(vna.query("*IDN?"))
    
    cal_check()
    # Query the frequency data for channel 1
    freq_array = vna.query('CALC1:DATA:STIM?')
    measurement_freq = np.fromstring(freq_array, sep=",")
    # initialise the Numpy array files for storing the data
    header = np.ones((1, (len(measurement_freq)+2)))
    header[0, 0] = time.time()
    header[0, 1] = chamber_temp  # hardcode a dummy temperature for now
    header[0, 2:] = measurement_freq
    # temporatory array used in formatting data
    temp = np.ones((1, (len(measurement_freq)+2)))
    # Use the header to create the zipped numpy array files
    for value in measurement_list:
        np.save(working_log_file +' %s.npy' % value, header)

    # selec the program
    tc.write('Programme en cours = "cable_stability"')
    # confirm that the correct program is selected
    # print(tc.query("?Programme en cours"))
    write_to_log_file(working_log_file,
                      'Programme selected on environmental chamber:'+ tc.query("?Programme en cours"))
    
    # Initiate the chamber
    tc.write('marche_arret = 1')  # this should start the programme
    time.sleep(20) # allow the program to start before interrogating
    # if (tc.query('?marche_arret') == ('marche_arret=1')):
    #     print('Environmental chamber turned on')
    #     write_to_log_file(working_log_file,'Environmental chamber turned on')
    # if (tc.query('?marche_arret') == ('marche_arret=0')):
    #     print('Environmental chamber turned off')
    environmental_tests_start_time = time.time()
    stop_time = environmental_tests_start_time + (15.5*60*60)
    # time_left = get_time_remaining()
    # if time_left == '':
    #     print('error receiving time left')
    # else:
    #     print('Time remaining in test: %2.3f h' % time_left)
    i=1
    while time.time() < stop_time:
        # Update the data in Numpy arrays with the measured data
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # TODO
        # Read the temperature from the environmental chamber
        chamber_temp = get_temperature(prev_value=chamber_temp)
        vna_data = capture_vna_data()
        # The time and chamber temp will be the same for all arrays
        temp[0, 0] = time.time()
        temp[0, 1] = chamber_temp
        for value in measurement_list:
            #  The VNA_measurement has the data correctly sorted
            # Add the vna data to the temp array
            temp[0, 2:] = vna_data[value]
            data = np.load(working_log_file +' %s.npy' % value)
            new_data = np.append(data, temp, axis=0)
            np.save(working_log_file +' %s.npy' % value, new_data)
        
        # time_left = get_time_remaining()
        # if time_left == '':
        #     print('error receiving time left')
        # else:
        #     print('Time remaining in test: %2.3f h' % time_left)
        
        # TODO - report the measurement progress
        print('Measurement %s' % i)
        write_to_log_file(working_log_file,
                      'Measurement %s' % i)
        write_to_log_file(working_log_file,chamber_temp)
        time.sleep(10) # 1 minute between tests will result in 7509 samples 
        i+=1
    # close the socket connections
    write_to_log_file(working_log_file,
                      'Test completed successfully')
    vna.close()
    tc.close()
except KeyboardInterrupt:
    
    tc.write('Annulation_essai = 0') # cancel the program
    write_to_log_file(working_log_file,
                      'cancelled by Keyboard interrupt')
    vna.close()
    tc.close()
except:
    write_to_log_file(working_log_file,
                      'cancelled by another exception')
    vna.close()
    tc.close()


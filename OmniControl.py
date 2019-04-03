#! /usr/bin/python

# Spencer Manning

# Import Libraries
import sys
import serial  # This gives access to the serial ports on the computer
import time
# import testrelayprotobuf_pb2   # Import the file compiled by the Protoc file
import numpy as np
import threading

# TODO: Receive ProtoBuf message from User in this code?

# Use this when working from the command line
# if len(sys.argv) < 2:
#     print "Not enough input variables \n Usage: OmniControl.py <Port> Eg. OmniControl.py COM1"
#     sys.exit(0)
#
# else:  # Example Input: relay on 0, relay on 1
#     portname = sys.argv[1]
#     relaycmd = sys.argv[2]
#     relaynum = sys.argv[3]

# Create a file for data input
filename = "calibrationoutputfile"
f = open(filename + '.txt', "w+")

# Temporary com port name until I start using the command line
# portname = 'COM3'  # This is for Windows
portname = '/dev/ttyACM0'  # This is for Linux

runtime = 2 # How long the noise source will be running

class Calibrate(object):
    # This class is for writing commands to the relay

    def __init__(self):
        # Open relay's serial port for communication
        self.serport = serial.Serial(portname, 9600, timeout=1)

    def noise_source(self):
        # Set up simulated noise into a 2xN array
        # This function will be replaced with the actual noise source's input data
        t = np.arange(0, runtime)
        amplitude = np.random.normal(-1, 1, runtime)
        noise = zip(t, amplitude)

        # Write Simulated Noise Data to the file
        f.write(str(time.strftime("Noise Data %Y%m%d_%H%M%S")) + "\n")
        for i in t:
            toimport = noise[i]
            f.write(str(toimport) + "\n")            
            time.sleep(1) #  Wait 1 second
            
            if i == runtime:
                exit("Finished uploading data")  # I think this only shows on the command line


    # Define RelayWrite function
    def calibrate(self, relaycmd, relaynum):

        print "Serial Port Name: ", self.serport.name  # ".name" comes from the imported "serial" library

        # Open relays: NS (Relay 0) and Switches (Relay 1)
        self.serport.write("relay " + str(relaycmd) + " " + str(relaynum) + "\n\r")  # Standard Numato command
        self.serport.write("relay " + str(relaycmd) + " " + str(relaynum + 1) + "\n\r")  # Standard Numato command
        print ("Noise Source is ON")
        print ("Switches are FLIPPED")    

        # Wait 5 seconds
        time.sleep(runtime)  # Run-time

        # Close relays: NS (Relay 0) and Switches (Relay 1)
        self.serport.write("relay " + "off" + " " + str(relaynum) + "\n\r")  # Standard Numato command
        self.serport.write("relay " + "off" + " " + str(relaynum + 1) + "\n\r")  # Standard Numato command

        self.serport.close()
        print ("Seral Port is closed")

# Collect noise source data for calibration
arr = ["on", 0]
Cal = Calibrate()  # Create an object

NoiseTh = threading.Thread(target=Cal.noise_source)
CalTh = threading.Thread(target=Cal.calibrate, args=(arr))

NoiseTh.start()
CalTh.start()

# TODO: Compute phase offsets from Calibration
#f = open(filename + '.txt', "r+")  # Open the file for updating.
data = f.readlines()  # Read all lines as a list


# TODO: Collect data again and use it to calculate angle of vehicle


# TODO:  Send data as message through ProtoBuf


# Close file

NoiseTh.join()
CalTh.join() 

#f.write('Done')  # Finish writing
f.close()
    
    
    
    
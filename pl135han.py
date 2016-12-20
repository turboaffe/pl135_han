import sys
import serial
import matplotlib.pyplot as plt
import numpy
import struct
import argparse
import warnings


parser = argparse.ArgumentParser(description='pl135han interface')
parser.add_argument('--interface')
parser.add_argument('--plot')
args = parser.parse_args()


if args.interface:
    interface = args.interface 
else:
    parser.print_help() 
    exit()

do_plot = False
if args.plot:
    do_plot = True


ser = serial.Serial(interface, 9600, timeout=1 )


temps = []
flows = []

# prepare plot only if requested
if do_plot:
    # turn on interactive plotting
    plt.ion()
    plt.autoscale(True)
    fig, (temp_axes, flow_axes) = plt.subplots(nrows=2, ncols=1)
    
    temp_axes.set_autoscale_on(True)
    flow_axes.set_autoscale_on(True)
    
    temp_plt, = temp_axes.plot(temps, temps)
    flow_plt, = flow_axes.plot(flows, flows)


while True:

    line = ser.readline()
   
    i = 0


    if len(line) == 40:



        flow_val, = struct.unpack('f', bytes([line[19], line[20], line[21], line[22]]))
        temp_val, = struct.unpack('f', bytes([line[23], line[24], line[25], line[26]]))

        print(str(flow_val) + ";" + str(temp_val))

        if do_plot:

            flows.append(flow_val)
            temps.append(temp_val)
    
            temp_plt.set_ydata(flows)
            temp_plt.set_xdata(list(range(len(flows))))
    
            flow_plt.set_ydata(temps)
            flow_plt.set_xdata(list(range(len(temps))))
    
            temp_axes.relim()
            temp_axes.autoscale_view(True, True, True)
            temp_axes.autoscale(True)
     
            flow_axes.relim()
            flow_axes.autoscale_view(True, True, True)
            flow_axes.autoscale(True)
            
            plt.draw()
            plt.pause(0.5)


ser.close()


# code for reverse engineering signal
#        for word in line:
#    
#            print(word, end="")
#            print("\t", end="")
#    
#            if i == int(sys.argv[1]):
#    
#                #save words in array
#                measurements.append(int(word))
#            
#                # for each word, calculate the diff
#                dif = numpy.diff(measurements)
#    
#                temp_plt.set_ydata(measurements)
#                temp_plt.set_xdata(list(range(len(measurements))))
#    
#                flow_plt.set_ydata(dif)
#                flow_plt.set_xdata(list(range(len(dif))))
#    
#    
#                axes.relim()
#                axes.autoscale_view(True, True, True)
#                
#                plt.draw()
#                plt.pause(0.5)
#    
#            i = i + 1
#    
#        print("")
 

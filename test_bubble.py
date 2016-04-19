import Adafruit_MCP3008
import BubblePlot as bp
import PressPlot2D as pp
import TempPlot2D as tp

import plotly.tools as tls
from plotly.graph_objs import *
import csv

import time
import datetime

class PUP():
    def __init__(self):
        self.init_chip()

    # Software SPI configuration:
    def init_chip(self):
        config_p1 = {'clk':2,'miso':3,'mosi':4,'cs':14}
        self.mcp_p1 = Adafruit_MCP3008.MCP3008(clk=config_p1['clk'], cs=config_p1['cs'], miso=config_p1['miso'], mosi=config_p1['mosi'])
        config_p2 = {'clk':15,'miso':18,'mosi':17,'cs':27}
        self.mcp_p2 = Adafruit_MCP3008.MCP3008(clk=config_p2['clk'], cs=config_p2['cs'], miso=config_p2['miso'], mosi=config_p2['mosi'])
        config_t1 = {'clk':22,'miso':23,'mosi':24,'cs':10}
        self.mcp_t1 = Adafruit_MCP3008.MCP3008(clk=config_t1['clk'], cs=config_t1['cs'], miso=config_t1['miso'], mosi=config_t1['mosi'])
        config_t2 = {'clk':9,'miso':11,'mosi':8,'cs':7}
        self.mcp_t2 = Adafruit_MCP3008.MCP3008(clk=config_t2['clk'], cs=config_t2['cs'], miso=config_t2['miso'], mosi=config_t2['mosi'])
        print("Chip Initialized!")

    def init_plots(self):
        stream_ids = tls.get_credentials_file()['stream_ids']
        self.bubble = bp.BubblePlot(stream_ids[0])

    def init_connections(self):
        self.bubble.init_stream()

    def close_connecntions(self):
        self.bubble.close_stream()

    def get_pressure(self,p):
        fsrVoltage = p/1023.0*5000 #Map from reading to 5v
        if(fsrVoltage==0):
            return 0
        elif (fsrVoltage == 5000):
            return 50   #Max pressure reached
        else:
            fsrResistance = 5000 - fsrVoltage
            fsrResistance = fsrResistance*100000/fsrVoltage   #10 k Resistor
            fsrConductance = 1000000/fsrResistance #Pulled from somewhere
            if(fsrConductance<=1000):
                fsrForce =fsrConductance/80.0
            else:
                fsrForce = (fsrConductance -1000.0)/30.0
            return fsrForce

    def read(self):
        # Main program loop.
        count=0
        values_p1 = [0]*8
        values_p2 = [0]*8
        values_t1 = [0]*8
        values_t2 = [0]*8
        while True:
            # Read all the ADC channel values in a list.
            for i in range(8):
                # The read_adc function will get the value of the specified channel (0-7).
                values_p1[i] = round(self.get_pressure(self.mcp_p1.read_adc(i)),4)
                values_p2[i] = round(self.get_pressure(self.mcp_p2.read_adc(i)),4)
                values_t1[i] = round(100*(self.mcp_t1.read_adc(i)/(1024/3.3))-50,1)
                values_t2[i] = round(100*(self.mcp_t2.read_adc(i)/(1024/3.3))-50,1)
            # Print the ADC values.
            print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values_p1))
            print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values_p2))
            print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values_t1))
            print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values_t2))
            print('-' * 57)

            # Send Values to plotly graphs
            temperature = values_t1+values_t2
            pressure = values_p1+values_p2

            self.bubble.send_value(pressure,temperature)
            time.sleep(0.5)

if __name__ == "__main__":
    pup = PUP()
    pup.init_plots()
    pup.init_connections()
    print("Reading Values...")
    pup.read()
    pup.close_connecntions()

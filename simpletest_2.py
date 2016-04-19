# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# Software SPI configuration:
CLK1  = 2
MISO1 = 3
MOSI1 = 4
CS1   = 14
mcp1 = Adafruit_MCP3008.MCP3008(clk=CLK1, cs=CS1, miso=MISO1, mosi=MOSI1)

CLK2  = 15
MISO2 = 18
MOSI2 = 17
CS2   = 27
mcp2 = Adafruit_MCP3008.MCP3008(clk=CLK2, cs=CS2, miso=MISO2, mosi=MOSI2)

CLK3  = 22
MISO3 = 23
MOSI3 = 24
CS3   = 10
mcp3 = Adafruit_MCP3008.MCP3008(clk=CLK3, cs=CS3, miso=MISO3, mosi=MOSI3)


CLK4  = 9
MISO4 = 11
MOSI4 = 8
CS4   = 7
mcp4 = Adafruit_MCP3008.MCP3008(clk=CLK4, cs=CS4, miso=MISO4, mosi=MOSI4)


print('Reading MCP3008 values, press Ctrl-C to quit...')
# Print nice channel column headers.
print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*range(8)))
print('-' * 57)
# Main program loop.
while True:
    # Read all the ADC channel values in a list.
    values1 = [0]*8
    values2 = [0]*8
    values3 = [0]*8
    values4 = [0]*8
    for i in range(8):
        # The read_adc function will get the value of the specified channel (0-7).
        values1[i] = mcp1.read_adc(i)
        values2[i] = mcp2.read_adc(i)
        #values3[i] = mcp3.read_adc(i)
        #values4[i] = mcp4.read_adc(i)
        values3[i] = round(100*(mcp3.read_adc(i)/(1024/3.3))-50,1)
        values4[i] = round(100*(mcp4.read_adc(i)/(1024/3.3))-50,1)

    # Print the ADC values.
    print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values1))
    print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values2))
    print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values3))
    print('| {0:>4} | {1:>4} | {2:>4} | {3:>4} | {4:>4} | {5:>4} | {6:>4} | {7:>4} |'.format(*values4))

    print('-' * 57)
    # Pause for half a second.
    time.sleep(0.5)

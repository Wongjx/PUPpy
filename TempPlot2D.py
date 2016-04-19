import plotly.plotly as py
import plotly.tools as tls
from plotly.graph_objs import *
import numpy as np  # (*) numpy for math functions and arrays
import time
import datetime

# def to_unix_time(dt):
#     epoch =  datetime.datetime.utcfromtimestamp(0)
#     return (dt - epoch).total_seconds() * 1000
# pressure = ['1','1','2']
# t = []
# for i in range(3):
#     #t.append(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'))
#     t.append(datetime.datetime.now())
#     # t.append(i)
#     time.sleep(0.01)
# Make instance of stream id object

class TempPlot2D():
    def __init__(self,stream_ids):
        self.stream_ids=stream_ids
        self.sensors =len(stream_ids)
        self.streams=[]
        self.prev_temp=[0]*self.sensors
        self.prev_time=datetime.datetime.now()

    def init_chart(self):
        data = []
        for i in range(self.sensors):
            stream = Stream(
                token=self.stream_ids[i],  # (!) link stream id to 'token' key
                maxpoints=20      # (!) keep a max of 80 pts on screen
            )
            data.append(dict(
                type='scatter',
                mode='lines',
                # x= time,
                # y= Temperature Differential,
                x=[],
                y=[],
                line=dict(
                    color=i,
                    width=4,
                ),
                stream=stream,
            ))

        layout = dict(
            title='2d Line Graph of Temperature Differential over Time',
            showlegend=False,
            scene=dict(
                xaxis=dict(title=''),
                yaxis=dict(title=''),
            )
        )
        fig = dict(data=data, layout=layout)
        url = py.plot(fig, filename='2d_temp')
        print ("Temperature Chart Initialized!")

    def init_stream(self):
        # Get stream id from stream id list
        # (@) Make instance of the Stream link object,
        #     with same stream id as Stream id object
        for i in range(self.sensors):
            s = py.Stream(self.stream_ids[i])
            s.open()
            self.streams.append(s)
        print ("Temp Stream Open!")

    def send_value(self,temp_readings):
        # Delay start of stream by 5 sec (time to switch tabs)
        new_time=datetime.datetime.now()
        
        for i in range(len(temp_readings)):
        
            diff=(temp_readings[i]-self.prev_temp[i])/((new_time-self.prev_time).total_seconds()) #Differential in degreeC/seconds
            
            #Threshold the value
            if(abs(diff)<1) or (abs(diff)>=5): #Limit values to between a 2 to 5 degree change per second to remove anomalies
                diff=0.0            
            
            data=dict(type='scatter',
                mode='lines',
                x=new_time,
                y=diff,
                )
            # (@) write to Plotly stream!
            self.streams[i].write(data)
            self.prev_temp[i]=temp_readings[i]
        self.prev_time=new_time
        # time.sleep(0.1)  # (!) plot a point every 80 ms, for smoother plotting

    def close_stream(self):
        # (@) Close the stream when done plotting
        for i in range(self.sensors):
            self.streams[i].close()
        self.streams=[]
        print ("Temp Stream Closed!")


if __name__ == '__main__':
    stream_ids = tls.get_credentials_file()['stream_ids']
    plot = TempPlot2D(stream_ids[17:34]);
    plot.init_chart()
    plot.init_stream()
    while True:
        temp_readings=np.random.uniform(25,28,size=16)
        plot.send_value(temp_readings)
        time.sleep(1)
    plot.close_stream()

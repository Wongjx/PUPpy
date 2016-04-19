# (*) To communicate with Plotly's server, sign in with credentials file
import plotly.plotly as py
# (*) Useful Python/Plotly tools
import plotly.tools as tls
# (*) Graph objects to piece together plots
import time
from plotly.graph_objs import *
import numpy as np  # (*) numpy for math functions and arrays

class BubblePlot():
    def __init__(self,stream_id):
        self.stream_id=stream_id

    def init_chart(self):
        # Make instance of stream id object
        stream = Stream(
            token=self.stream_id,  # (!) link stream id to 'token' key
            maxpoints=20      # (!) keep a max of 80 pts on screen
        )
        # Initialize trace of streaming plot by embedding the unique stream_id
        trace1 = Scatter(
            x=[1,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4],
            y=[1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4],
            mode='markers',
            marker=dict(
                size=[],
                color=[],
            ),
            text=[],
            stream=stream,
        )
        data = Data([trace1])
        # Add title to layout object
        layout = Layout(title='Realtime Visualization of Pressure and Temperature Readings',xaxis=dict(tickmode='array',tickvals=[1,2,3,4]) ,yaxis=dict(tickmode='array',tickvals=[1,2,3,4]))
        fig = Figure(data=data, layout=layout)
        unique_url = py.plot(fig, filename='Pressure and Temperature Reading')
        print("Bubble Chart Initialized!")

    def init_stream(self):
        # (@) Make instance of the Stream link object,
        #     with same stream id as Stream id object
        self.stream = py.Stream(self.stream_id)
        # (@) Open the stream
        self.stream.open()
        print("Bubble Stream Open!")

    def close_stream(self):
        # (@) Close the stream when done plotting
        self.stream.close()
        print("Bubble Stream Closed!")

    def send_value(self,pressure,temperature):
        text=[]
        size=[]
        color=[]
        for i in range(16):
            if (pressure[i]>=50):
                size.append(50)
            elif(pressure[i]<=1):
                size.append(10)
            else:
                size.append(10+(pressure[i]/50.0*40)) #Map pressure value into range from 1 to 5
            c = self.get_color(temperature[i])
            color.append("rgb({0}, {1}, {2})".format(c[0],c[1],c[2]));
            text.append("Pressure : {0} kgm^2\nTemperature : {1}".format(pressure[i],temperature[i]))
        self.stream.write(dict(text=text,marker=dict(size=size,color=color)))

    def get_color(self,temperature):
        if (temperature>29.0):
            return (255,0,0)
        elif (temperature>28.0):
            return (255,128,0)
        elif(temperature>27.0):
            return (255,255,0)
        else:
            return (128,255,0)

if __name__ == '__main__':
    stream_ids = tls.get_credentials_file()['stream_ids']
    b = BubblePlot(stream_ids[0]);
    b.init_chart()
    b.init_stream()
    while True:
        pressure = np.random.uniform(0,100,size=16)
        temperature = np.random.uniform(25,30,size=16)
        b.send_value(pressure,temperature)
    b.close_stream()

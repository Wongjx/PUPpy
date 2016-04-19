import plotly.plotly as py
import plotly.tools as tls
from plotly.graph_objs import *
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

class PressPlot2D():
    def __init__(self,stream_ids):
        self.stream_ids=stream_ids
        self.sensors =len(stream_ids)
        self.streams=[]
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
                # x= t,
                # y= pressure,
                x=[],
                y=[],
                line=dict(
                    color=i,
                    width=4,
                ),
                stream=stream,
            ))

        layout = dict(
            title='2d Line Graph of Pressure over Time',
            showlegend=False,
            scene=dict(
                xaxis=dict(title=''),
                yaxis=dict(title=''),
            )
        )

        fig = dict(data=data, layout=layout)
        url = py.plot(fig, filename='2d_press')
        print ("Pressure Chart Intialized!")

    def init_stream(self):
        # Get stream id from stream id list
        # (@) Make instance of the Stream link object,
        #     with same stream id as Stream id object
        for i in range(len(self.stream_ids)):
            s = py.Stream(self.stream_ids[i])
            s.open()
            self.streams.append(s)
        print("Pressure Stream Open!")

    def send_value(self,pressure_readings):
        # Delay start of stream by 5 sec (time to switch tabs)
        # time.sleep(5)
        tn=datetime.datetime.now()
        for i in range(len(pressure_readings)):
            data=dict(type='scatter',
                mode='lines',
                x=tn,
                y=pressure_readings[i],
                )
            self.streams[i].write(data)
        # time.sleep(0.1)  # (!) plot a point every 80 ms, for smoother plotting

    def close_stream(self):
        # (@) Close the stream when done plotting
        for i in range(len(self.streams)):
            self.streams[i].close()
        self.streams=[]
        print("Pressure Streams Closed!")

if __name__ == '__main__':
    stream_ids = tls.get_credentials_file()['stream_ids']
    plot = PressPlot2D(stream_ids[1:17]);
    plot.init_chart()
    plot.init_stream()
    while True:
        pressure_readings = np.random.uniform(0,100,size=16)
        plot.send_value(pressure_readings)
        time.sleep(0.5)

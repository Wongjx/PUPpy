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
        #self.init_chip()
        return

    def init_plots(self):
        stream_ids = tls.get_credentials_file()['stream_ids']
        self.bubble = bp.BubblePlot(stream_ids[0])
        self.bubble.init_chart()
        self.press = pp.PressPlot2D(stream_ids[1:17])
        self.press.init_chart()
        self.temp = tp.TempPlot2D(stream_ids[17:34])
        self.temp.init_chart()


if __name__ == "__main__":
    pup = PUP()
    pup.init_plots()

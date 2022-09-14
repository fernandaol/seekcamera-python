from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

plt.style.use('fivethirtyeight')

x_vals = []
y_vals = []

index = count()

def animate(i):
    data = pd.read_csv('data.csv')
    x = data['x_value']
    y1 = data['minimum_value']
    y2 = data['meantemp_value']
    y3 = data['maximum_value']

    plt.cla()
    plt.rcParams["figure.autolayout"] = True

    plt.plot(x, y1, label='Minimum')
    plt.plot(x, y2, label='Mean')
    plt.plot(x, y3, label='Maximum')

    plt.legend(loc='upper left')
    plt.tight_layout()

    # fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, sharex=True)
    # ax1.plot(x, y1, label='Min')
    # ax1.legend(loc='upper left')
    # ax1.set_title('MIN Temperature over Time')
    #
    # print("Foi 1")
    #
    # ax2.plot(x, y2, 'tab:orange', label='Average')
    # ax2.legend(loc='upper left')
    # ax2.set_title('AVERAGE of Temperatures over Time')
    #
    # print("Foi 2")
    #
    # ax3.plot(x, y3, 'tab:green', label='Max')
    # ax3.legend(loc='upper left')
    # ax3.set_title('MAX Temperature over Time')
    #
    # print("Foi 3")

#interval: time in miliseconds, how often we want to run the function 'animate'

ani = FuncAnimation(plt.gcf(), animate, interval=1000)
plt.tight_layout()
plt.show()

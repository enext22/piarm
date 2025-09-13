# test supplier ultrasonic driver

from robot_hat import Ultrasonic, Pin
from time import sleep
from matplotlib import pyplot, animation
import datetime as dt

trig = Pin("D0")
echo = Pin("D1")

hc_sr04 = Ultrasonic(trig, echo)


fig = pyplot.figure()
ax = fig.add_subplot(1, 1, 1)
time = []
data = []

def animate_readings(i, time, data):

    dist = hc_sr04.read()

    time.append(dt.datetime.now().strftime('%S.%f'))
    data.append(dist)

    # SLIDING WINDOW FOR PLOTS
    time = time[-20:]
    data = data[-20:]

    ax.clear()
    ax.plot(time, data)

    # FORMATTING
    pyplot.xticks(rotation=45, ha='right')
    pyplot.subplots_adjust(bottom=0.30)
    pyplot.title('HC-SR04 Distance over Time')
    pyplot.ylabel('Distance (cm)')
    pyplot.ylim(0, 20) #define fixed limits for graph to aid in visualization


animated = animation.FuncAnimation(fig, animate_readings, fargs=(time, data), interval=1000)
pyplot.show()

#while True:
#    val = hc_sr04.read()
#    animate_readings(time, data, val)
#    print(val)
#    sleep(1)

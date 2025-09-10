# test supplier ultrasonic driver

from robot_hat import Ultrasonic, Pin
from time import sleep

trig = Pin("D0")
echo = Pin("D1")

hc_sr04 = Ultrasonic(trig, echo)

while True:
    val = hc_sr04.read()
    print(val)
    sleep(0.1)

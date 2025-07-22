from robot_hat import Servo,PWM,Joystick,ADC,Pin
from robot_hat.utils import reset_mcu
from time import sleep
import logging
import RPi.GPIO as GPIO

from piarm import PiArm


logging.basicConfig(level=logging.ERROR)

reset_mcu()
sleep(0.01)

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(17, GPIO.IN) #D0
#GPIO.setup(4, GPIO.IN) #D1

leftJoystick = Joystick('A0','A1',17)
rightJoystick = Joystick('A2','A3',4)
arm = PiArm(['P0','P1','P2'])
arm.hanging_clip_init(PWM('P3'))
arm.set_offset([0,0,0])

def _angles_control():
    arm.speed = 100
    flag = False
    alpha,beta,gamma = arm.servo_positions
    clip = arm.component_staus

    x_val = ADC('A0').read()
    y_val = ADC('A1').read()

    #print(f'DEFAULT X IS {x_val}')
    #print(f'DEFAULT Y IS {y_val}')
    #sleep(5)

    if leftJoystick.read_status_y() == "up":
        alpha += 1
        flag = True
    elif leftJoystick.read_status_y() == "down":
        alpha -= 1
        flag = True
    #elif leftJoystick.read_status_y() == "stall":
    #    flag = False

    if leftJoystick.read_status_x() == "left":
        gamma += 1
        flag = True
    elif leftJoystick.read_status_x() == "right":
        gamma -= 1
        flag = True
    #elif leftJoystick.read_status_x() == "stall":
    #    flag = False


    if rightJoystick.read_status_y() == "up":
        beta += 1
        flag = True
    elif rightJoystick.read_status_y() == "down":
        beta -= 1
        flag = True
    #elif rightJoystick.read_status_y() == "stall":
    #    flag = False
        
    if leftJoystick.read_status_b() == "pressed": 	
        clip += 2
        flag = True
    elif rightJoystick.read_status_b() == "pressed":	
        clip -= 2
        flag = True
    #else:
    #    flag = False

    if flag == True:
        arm.set_angle([alpha,beta,gamma])
        arm.set_hanging_clip(clip)
        print('servo angles: %s , clip angle: %s '%(arm.servo_positions,arm.component_staus))

if __name__ == "__main__":
    while True:
        _angles_control()
        sleep(0.01)
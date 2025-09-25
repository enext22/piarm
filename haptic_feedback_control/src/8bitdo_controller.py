# RUN FILE FROM CLI WITH 'xvfb-run python [NAME].py' if accessing over ssh with no physical display connected

from robot_hat import Pin, Ultrasonic
from robot_hat.utils import reset_mcu
from time import sleep
import logging
import pygame
import sys
from controller_functions import init_arm, _angles_control



########### BASIC INITIALIZATIONS ###########
logging.basicConfig(level=logging.ERROR)
reset_mcu()
sleep(0.01)
use_dist_sensor = False

arm = init_arm()

EE_default_angle_increment = 2
EE_angle_increment = 2 # End-effector angle increment
proceed = True
##############################################


########### CHECK CLI ARGUMENTS FOR SENSOR USE ###########
if len(sys.argv) > 1:
    arg_1 = sys.argv[1]

    if arg_1 == '--dist' or arg_1 == '-d':  
        print("\n### Using Distance Sensor ###\n")
        use_dist_sensor = True
        RANGE_MAX = 7 # 6cm limit for basic object detection
        RANGE_TARGET = 5
        trig = Pin("D0")
        echo = Pin("D1")
##########################################################


########### SETUP 8BITDO CONTROLLER ###########
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
print(joysticks)

pygame.init()
pygame.joystick.Joystick(0).init()
bitdo = pygame.joystick.Joystick(0)
clock = pygame.time.Clock()
###############################################


############## INITIALIZE SENSOR ##############
if use_dist_sensor:
    # setup distance sensor
    hcsr04 = Ultrasonic(trig, echo)
###############################################



while proceed:
    # Scan through 8bitdo controller inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           break
        if pygame.joystick.Joystick(0).get_button(6):
           # pressing minus button on the controller an exit and teardown of code
           proceed = False
           print("### User Exited Process ###")
           break

        # Optional logging to determine which events are being triggered by new inputs on the 8bitdo
        if logging.getLevelName == logging.DEBUG:
            if event.type == pygame.JOYBUTTONDOWN:
                # Print statement provides event reference which can be used/watched above to add new functionality
                print(f'\nPygame Joystick Event: {event}')


    # Retrieve adjusted values from 8bitdo joycons
    x_val_left = round(bitdo.get_axis(0))
    y_val_left = round(bitdo.get_axis(1))

    x_val_right = round(bitdo.get_axis(3))
    y_val_right = round(bitdo.get_axis(4))
    
    # Compute new piarm angles based on tilt of joycons
    _angles_control(arm, bitdo, EE_angle_increment, x_val_left, y_val_left, x_val_right, y_val_right)
    sleep(0.01)

    # Calcualte grip adjustment for end-effector and rumble scale based on target proximity
    if use_dist_sensor:
        # if arm end-effector is in range of objects
        dist = hcsr04.read()
        if (dist < RANGE_MAX): #and (arm.component_staus < -20):
            # rumble controller
            high_freq = (RANGE_MAX - round(dist))*0.1 # subtracting from limit because we want the LOWER sensor readings to trigger HIGHER vibration
            low_freq = (high_freq - 0.2) if high_freq > 0.2 else 0.1 # low_freq defaults to lowest setting 0.1 if distance from object is high

            if high_freq < 0.2: high_freq = 0.2

            bitdo.rumble(low_freq, high_freq, 1000) # rumble for 1s at specified frequencies in range [0, 1]
            print(f'\nRumble Min: {low_freq}, Rumble Max: {high_freq}')

            # additionally we must ADJUST the speed of change of our clip
            ratio = abs(RANGE_TARGET - dist)/RANGE_MAX
            EE_angle_increment = EE_default_angle_increment * ratio #
            print(f'New EE angle increment is: {EE_angle_increment}')

        else:
            # stop rumble
            bitdo.stop_rumble()
            # reset EE_angle_increment
            EE_angle_increment = EE_default_angle_increment


    clock.tick(180)

# Perform Teardown
# Return to origin position
arm.set_angle([0,0,0])
arm.set_hanging_clip(-40) # fully opened clip, otherwise causes false triggers of ultrasonic from clip frame

pygame.quit()

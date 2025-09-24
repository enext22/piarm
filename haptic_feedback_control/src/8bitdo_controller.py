# RUN FILE FROM CLI WITH 'xvfb-run python [NAME].py' if accessing over ssh with no physical display connected

from robot_hat import Servo, PWM, ADC, Pin, Ultrasonic
from robot_hat.utils import reset_mcu
from time import sleep
import logging
import RPi.GPIO as GPIO
import pygame
import sys
import controller_functions

from piarm import PiArm


logging.basicConfig(level=logging.ERROR)

reset_mcu()
sleep(0.01)


use_dist_sensor = False

if len(sys.argv) > 1:
    arg_1 = sys.argv[1]

    if arg_1 == '--dist' or arg_1 == '-d':  
        print("\n### Using Distance Sensor ###\n")
        use_dist_sensor = True
        RANGE_MAX = 7 # 6cm limit for basic object detection
        RANGE_TARGET = 5
        trig = Pin("D0")
        echo = Pin("D1")

def init_arm():
    arm = PiArm(['P0','P1','P2'])
    arm.hanging_clip_init(PWM('P3'))
    arm.set_offset([0,0,0])

    return arm

arm = init_arm()

EE_default_angle_increment = 2
EE_angle_increment = 2 # End-effector angle increment

def _angles_control(x_val_left, y_val_left, x_val_right, y_val_right):

    arm.speed = 300
    flag = False
    alpha,beta,gamma = arm.servo_positions
    clip = arm.component_staus


    if(y_val_left > 0): # moving DOWN on left stick
        alpha -= 5
        flag = True
    elif(y_val_left < 0): # moving UP on left stick
        alpha += 5
        flag = True

    if(x_val_left > 0): # moving RIGHT on left stick
        gamma -= 5
        flag = True
    elif(x_val_left < 0): # moving LEFT on left stick
        gamma += 5
        flag = True


    if(y_val_right > 0): # moving DOWN on right stick
        beta -= 5
        flag = True
    elif(y_val_right < 0): # moving UP on right stick
        beta += 5
        flag = True

    if pygame.joystick.Joystick(0).get_button(2): # X button is pressed
        clip += EE_angle_increment
        flag = True
    elif pygame.joystick.Joystick(0).get_button(1): # B button is pressed	
        clip -= EE_default_angle_increment
        flag = True


    if flag == True:
        arm.set_angle([alpha,beta,gamma])
        arm.set_hanging_clip(clip)
        print('\nx_val_left: %d, y_val_left: %d,   x_val_right: %d, y_val_right: %d' %(x_val_left, y_val_left, x_val_left, y_val_left))
        print('\nClip Angle Adjustment: %d', clip)
        logging.debug('\nServo angles: %s , Clip angle: %s '%(arm.servo_positions,arm.component_staus))


pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
print(joysticks)

pygame.init()
pygame.joystick.Joystick(0).init()
clock = pygame.time.Clock()

status = True

if use_dist_sensor:
    # setup distance sensor
    hcsr04 = Ultrasonic(trig, echo)


while status:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           break
        if pygame.joystick.Joystick(0).get_button(6):
           # press minus button on the controller
           status = False
           print("### User Exited Process ###")
           break

        if logging.getLevelName == logging.DEBUG:
            if event.type == pygame.JOYBUTTONDOWN:
                print(f'\nPygame Joystick Event: {event}')

    x_val_left = round(pygame.joystick.Joystick(0).get_axis(0))
    y_val_left = round(pygame.joystick.Joystick(0).get_axis(1))

    x_val_right = round(pygame.joystick.Joystick(0).get_axis(3))
    y_val_right = round(pygame.joystick.Joystick(0).get_axis(4))

    _angles_control(x_val_left, y_val_left, x_val_right, y_val_right)
    sleep(0.01)

    if use_dist_sensor:
        # if arm end-effector is in range of objects
        dist = hcsr04.read()
        if (dist < RANGE_MAX): #and (arm.component_staus < -20):
            # rumble controller
            high_freq = (RANGE_MAX - round(dist))*0.1 # subtracting from limit because we want the LOWER sensor readings to trigger HIGHER vibration
            low_freq = (high_freq - 0.2) if high_freq > 0.2 else 0.1 # low_freq defaults to lowest setting 0.1 if distance from object is high

            if high_freq < 0.2: high_freq = 0.2

            pygame.joystick.Joystick(0).rumble(low_freq, high_freq, 1000) # rumble for 1s at specified frequencies in range [0, 1]
            print(f'\nRumble Min: {low_freq}, Rumble Max: {high_freq}')

            # additionally we must ADJUST the speed of change of our clip
            ratio = abs(RANGE_TARGET - dist)/RANGE_MAX
            EE_angle_increment = EE_default_angle_increment * ratio #
            print(f'\nNew EE angle increment is: {EE_angle_increment}')

        else:
            # stop rumble
            pygame.joystick.Joystick(0).stop_rumble()
            # reset EE_angle_increment
            EE_angle_increment = EE_default_angle_increment


    clock.tick(180)

# Return to origin position
arm.set_angle([0,0,0])
arm.set_hanging_clip(-40) # fully opened clip, otherwise causes false triggers of ultrasonic from clip frame

pygame.quit()

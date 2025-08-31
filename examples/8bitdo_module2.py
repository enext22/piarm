# RUN FILE FROM CLI WITH 'xvfb-run python [NAME].py' if accessing over ssh with no physical display connected

from robot_hat import Servo,PWM,Joystick,ADC,Pin
from robot_hat.utils import reset_mcu
from time import sleep
import logging
import RPi.GPIO as GPIO
import pygame
import sys

from piarm import PiArm


logging.basicConfig(level=logging.ERROR)

reset_mcu()
sleep(0.01)

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(17, GPIO.IN) #D0
#GPIO.setup(4, GPIO.IN) #D1

#leftJoystick = pygame.joystick.Joystick(0)
#rightJoystick = pygame.joystick.Joystick(0)

arm = PiArm(['P0','P1','P2'])
arm.hanging_clip_init(PWM('P3'))
arm.set_offset([0,0,0])

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
        clip += 2
        flag = True
    elif pygame.joystick.Joystick(0).get_button(1): # B button is pressed	
        clip -= 2
        flag = True



    if flag == True:
        arm.set_angle([alpha,beta,gamma])
        arm.set_hanging_clip(clip)
        print('x_val_left: %d, y_val_left: %d,   x_val_right: %d, y_val_right: %d' %(x_val_left, y_val_left, x_val_left, y_val_left))
        #print(arm.servo_positions)
        #print('servo angles: %s , clip angle: %s '%(arm.servo_positions,arm.component_staus))

#if __name__ == "__main__":

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
print(joysticks)

pygame.init()
pygame.joystick.Joystick(0).init()
clock = pygame.time.Clock()

# low freq [0,1], high frequency [0,1], duration in ms
# can scale vibration intensity as a function of distance from target
# along with SLOWING the grab motor
pygame.joystick.Joystick(0).rumble(0.1, 0.3, 1000) # rumble for 1s
sleep(1)
pygame.joystick.Joystick(0).stop_rumble()

status = True

while status:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           break
        if pygame.joystick.Joystick(0).get_button(6):
	   # press minus button on the controller
           status = False
           print("### User Exited Process ###")
           break
        #if event.type == pygame.JOYBUTTONDOWN:
           #print(event)

    x_val_left = round(pygame.joystick.Joystick(0).get_axis(0))
    y_val_left = round(pygame.joystick.Joystick(0).get_axis(1))

    x_val_right = round(pygame.joystick.Joystick(0).get_axis(3))
    y_val_right = round(pygame.joystick.Joystick(0).get_axis(4))
    #print('x_val_left: %d, y_val_left: %d' %(x_val_left, y_val_left))
    _angles_control(x_val_left, y_val_left, x_val_right, y_val_right)
    sleep(0.01)

    # if arm end-effector is in range of objects
    # trigger rumble effect
    # stop rumble effect

    clock.tick(180)

pygame.quit()

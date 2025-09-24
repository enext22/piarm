from piarm import PiArm
from robot_hat import PWM
import logging

def init_arm():
    arm = PiArm(['P0','P1','P2'])
    arm.hanging_clip_init(PWM('P3'))
    arm.set_offset([0,0,0])

    return arm

def _angles_control(arm, joystick, EE_increment, x_val_left, y_val_left, x_val_right, y_val_right):

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

    if joystick.get_button(2): # X button is pressed
        clip += EE_increment
        flag = True
    elif joystick.get_button(1): # B button is pressed	
        clip -= 2
        flag = True


    if flag == True:
        arm.set_angle([alpha,beta,gamma])
        arm.set_hanging_clip(clip)
        print('\nx_val_left: %d, y_val_left: %d,   x_val_right: %d, y_val_right: %d' %(x_val_left, y_val_left, x_val_left, y_val_left))
        print('\nClip Angle Adjustment: %d', clip)
        logging.debug('\nServo angles: %s , Clip angle: %s '%(arm.servo_positions,arm.component_staus))

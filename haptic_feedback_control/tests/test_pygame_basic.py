import pygame
from src.pygame_basic import init_pygame

# simple pytest function to validate pytest structure in application

def test_init_pygame():
    # validate that the appropriate controller is connected
    controller, user, clock, screen = init_pygame()
    assert controller == pygame.joystick.Joystick(0)
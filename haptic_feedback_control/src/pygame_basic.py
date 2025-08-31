import pygame
import pytest


class Player(object):

	def __init__(self):
		self.player = pygame.rect.Rect((300,400, 50, 50))
		self.color = "white"

	def move(self, x_speed, y_speed):
		self.player.move_ip((x_speed, y_speed))

	def change_color(self, color):
		self.color = color

	def draw(self, game_screen):
		pygame.draw.rect(game_screen, self.color, self.player)

def init_pygame():
	pygame.joystick.init()
	joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
	print(joysticks)

	pygame.init()
	player = Player()
	clk = pygame.time.Clock()
	disp = pygame.display.set_mode((800,600))

	pygame.joystick.Joystick(0).init()

	return pygame.joystick.Joystick(0), player, clk, disp

if __name__ == "__main__":

	controller, user, clock, screen = init_pygame()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				break
			if event.type == pygame.JOYBUTTONDOWN:
				
				if controller.get_button(2):
					user.change_color("blue")
				elif controller.get_button(1):
					user.change_color("red")
				elif controller.get_button(0):
					user.change_color("green")
				elif controller.get_button(3):
					user.change_color("yellow")

		x_speed = round(controller.get_axis(3))
		y_speed = round(controller.get_axis(4))
		#print(f'x-value: {x_speed}, y-value: {y_speed}')
		user.move(x_speed, y_speed)

		screen.fill((0,0,0))
		user.draw(screen)
		pygame.display.update()
		clock.tick(180)

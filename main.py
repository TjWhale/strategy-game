# This is the main file for the game and everything branches off here.
# When writing code please try to write it for the next person to work on it.
# That means please try to be tidy and organised and write plenty of comments.
# You want to feel like you're explaining to the next person what your code does and how to improve it later.

import pygame
import math
import random
from pygame.locals import *

from world_map_file import world_map_class
from gui_file import gui_class

# Setup the screen, it's important that later we'll probably want to use fullscreen.
# So please scale everything to screen_width and screen_height.

background_colour = (0,0,0)
(screen_width, screen_height) = (1000, 600)

screen = pygame.display.set_mode((screen_width, screen_height))#,pygame.FULLSCREEN)

pygame.display.set_caption('Untitled Strategy Game')
pygame.font.init()

# Fonts will def need some work as this one is very basic.

myfont = pygame.font.SysFont("monospace", 20)

pygame_clock = pygame.time.Clock()

# These are the main game objects which are imported from their relevant files above.

world_map = world_map_class()  # This is the background hex map.
gui = gui_class() # This is the gui on the screen on top of the hex map.
popup = False # If any other screen is in view it's a popup on top of everything else.
# If a popup is in action the rest of the screen cannot be clicked on until the popup is closed.


running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == KEYDOWN:
			if event.key == K_ESCAPE:
				running = False

	       

	screen.fill(background_colour)

	world_map.draw(screen)
	gui.draw(screen)
	if popup:
		popup.draw(screen)

	pygame.display.flip()

	#print("frame time ms = ", pygame_clock.get_time())
	pygame_clock.tick(60)

pygame.quit()
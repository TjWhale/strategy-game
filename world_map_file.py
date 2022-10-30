# This file contains the world map class which is the large hex grid on which the game is played.
# It needs to be able to generate itself, draw itself and keep track of units an cities.

import pygame

class world_map_class:
	def __init__(self):
		self.position = [0,0,100,100]

	def draw(self, screen):
		pygame.draw.rect(screen, [255,0,0], self.position)
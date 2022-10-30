# This file contains the gui class which overlays the world map.

import pygame

class gui_class:
	def __init__(self):
		self.position = [0,0,200,30]

	def draw(self, screen):
		pygame.draw.rect(screen, [0,0,255], self.position)
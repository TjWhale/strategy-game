# This file contains the world map class which is the large hex grid on which the game is played.
# It needs to be able to generate itself, draw itself and keep track of units an cities.

import pygame
import random


tile_plain = pygame.image.load("tiles/tile_plane.png").convert_alpha()

class world_map_class:
	def __init__(self, map_size):
		self.map_size = map_size
		self.tile_image_size = [64,32] #set the global size of the tile images
		self.tiles = []

		#add the tiles to an array
		for i in range(map_size[0]):
			self.tiles.append([])
			for j in range(map_size[1]):
				self.tiles[i].append(world_map_tile(i,j, self.tile_image_size))

		#parameters for drawing the map
		self.origin_coordinates = [200,100]
		self.zoom_level = 1

	#given some coordinates for the center of the screen and a zoom level draw the map
	def draw(self, screen):
		for tile_line in self.tiles:
			for tile in tile_line:
				tile.draw(screen, self.origin_coordinates, self.zoom_level)

	def mouse_click(self, position):
		print("You clicked on the map")

class world_map_tile:
	def __init__(self, i, j, tile_image_size):
		self.i = i #x coordinate of the tile in the grid
		self.j = j #y coordinate of the tile in the grid

		self.tile_image_size = tile_image_size #how big is the tile image in pixels?

		self.x = 200 #the current coordinates of the top left of the tile relative to scrolling and zooming
		self.y = 200

	def draw(self, screen, origin_coordinates, zoom_level):
		#compute your relative top left corner
		self.x = 0.75*self.i*self.tile_image_size[0] - origin_coordinates[0]
		self.y = self.j*self.tile_image_size[1] - origin_coordinates[1]
		if self.i % 2 == 1:
			self.y += self.tile_image_size[1]/2

		#draw a polygon at that position
		points = self.get_polygon_points()
		pygame.draw.polygon(screen, [250,0,0], points, int(2))

	def get_polygon_points(self):
		points = [[self.x + 0.25*self.tile_image_size[0], self.y], 
				[self.x + 0.75*self.tile_image_size[0], self.y], 
				[self.x + self.tile_image_size[0], self.y + 0.5*self.tile_image_size[1]], 
				[self.x + 0.75*self.tile_image_size[0], self.y + self.tile_image_size[1]], 
				[self.x + 0.25*self.tile_image_size[0], self.y + self.tile_image_size[1]], 
				[self.x, self.y + 0.5*self.tile_image_size[1]]]

		return points



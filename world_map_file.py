# This file contains the world map class which is the large hex grid on which the game is played.
# It needs to be able to generate itself, draw itself and keep track of units an cities.

import pygame
import random

tile_plain = pygame.image.load("tiles/tile_plane.png").convert_alpha()
tile_deep_ocean = pygame.image.load("tiles/tile_deep_ocean.png").convert_alpha()
tile_shallow_ocean = pygame.image.load("tiles/tile_shallow_ocean.png").convert_alpha()
tile_desert = pygame.image.load("tiles/tile_desert.png").convert_alpha()
tile_human_grass = pygame.image.load("tiles/tile_human_grass.png").convert_alpha()

class world_map_class:
	def __init__(self, map_size):
		self.map_size = map_size
		self.tile_image_size = [64,32] #set the global size of the tile images
		#the actual images are [64,48] because there is space on the top 
		#this has to be accounted for when drawing
		self.tile_image_height_offset = 16
		self.tiles = []

		#add the tiles to an array
		for i in range(map_size[0]):
			self.tiles.append([])
			for j in range(map_size[1]):
				self.tiles[i].append(world_map_tile(i,j, self.tile_image_size))

		self.check_tile_tags_for_clashes()

		#parameters for drawing the map
		self.origin_coordinates = [200,100]
		self.zoom_level = 1

	#given some coordinates for the center of the screen and a zoom level draw the map
	def draw(self, screen):
		for tile_line in self.tiles:
			for tile in tile_line:
				tile.draw(screen, self.origin_coordinates, self.zoom_level, self.tile_image_height_offset)

	def mouse_click(self, event):
		print("You clicked on the map")
		if event.type == pygame.MOUSEBUTTONDOWN:
			#zoom the screen with the scroll wheel
			if event.button == 4:
				if self.zoom_level < 4:
					self.zoom_level = min(4, self.zoom_level+1)

			elif event.button == 5:
				if self.zoom_level > 1:
					self.zoom_level = max(1, self.zoom_level-1)

	def mouse_hover(self, screen, delta_time):
		#scroll the screen if the mouse is near the edge
		mouse_pos = pygame.mouse.get_pos()
		screen_size = screen.get_size()
		scroll_speed = 0.4*delta_time/self.zoom_level
		if mouse_pos[0] < 50:
			self.origin_coordinates[0] -= scroll_speed
		if mouse_pos[0] > screen_size[0] - 50:
			self.origin_coordinates[0] += scroll_speed
		if mouse_pos[1] < 50:
			self.origin_coordinates[1] -= scroll_speed
		if mouse_pos[1] > screen_size[1] - 50:
			self.origin_coordinates[1] += scroll_speed

		#make sure that the origin is at an integer value for pixel perfect
		self.origin_coordinates[0] = int(self.origin_coordinates[0])
		self.origin_coordinates[1] = int(self.origin_coordinates[1])

	#look through all the tiles and make sure they don't have mixed tags, like "desert" and "deep ocean" at the same time
	def check_tile_tags_for_clashes(self):
		#list of combinations of tags which can't happen at the same time
		forbidden_combinations = [["plain", "desert", "deep ocean", "shallow ocean", "human grass"]]
		for forbidden_combination in forbidden_combinations:
			for tile_line in self.tiles:
				for tile in tile_line:
					if sum(x in tile.tile_tags for x in forbidden_combination) > 1:
						print("Error, duplicates detected in the tile_tags of tile", tile.i, ", ", tile.j, ". Tags are ", tile.tile_tags)



class world_map_tile:
	def __init__(self, i, j, tile_image_size):
		self.i = i #x coordinate of the tile in the grid
		self.j = j #y coordinate of the tile in the grid

		self.tile_image_size = tile_image_size #how big is the tile image in pixels?

		self.x = 0 #the current coordinates of the top left of the tile relative to scrolling and zooming
		self.y = 0

		self.tile_tags = [] #this contains a list of tags which determine what the tile is
		self.tile_tags.append(random.choice(["plain", "desert", "deep ocean", "shallow ocean", "human grass"]))

	def draw(self, screen, origin_coordinates, zoom_level, tile_image_height_offset):
		#compute your relative top left corner
		screen_size = screen.get_size()
		self.x = (0.75*self.i*self.tile_image_size[0] - origin_coordinates[0])*zoom_level + screen_size[0]/2
		self.y = (self.j*self.tile_image_size[1] - origin_coordinates[1])*zoom_level + screen_size[1]/2
		if self.i % 2 == 1:
			self.y += self.tile_image_size[1]*zoom_level/2

		#draw a polygon at that position
		#points = self.get_polygon_points()
		#pygame.draw.polygon(screen, [250,0,0], points, int(2))
		base_terrain = tile_plain
		if "desert" in self.tile_tags:
			base_terrain = tile_desert
		if "deep ocean" in self.tile_tags:
			base_terrain = tile_deep_ocean
		if "shallow ocean" in self.tile_tags:
			base_terrain = tile_shallow_ocean
		if "human grass" in self.tile_tags:
			base_terrain = tile_human_grass
		drawn_tile = pygame.transform.rotozoom(base_terrain, 0, zoom_level)
		screen.blit(drawn_tile, (self.x, self.y - tile_image_height_offset*zoom_level))

	def get_polygon_points(self):
		points = [[self.x + 0.25*self.tile_image_size[0], self.y], 
				[self.x + 0.75*self.tile_image_size[0], self.y], 
				[self.x + self.tile_image_size[0], self.y + 0.5*self.tile_image_size[1]], 
				[self.x + 0.75*self.tile_image_size[0], self.y + self.tile_image_size[1]], 
				[self.x + 0.25*self.tile_image_size[0], self.y + self.tile_image_size[1]], 
				[self.x, self.y + 0.5*self.tile_image_size[1]]]

		return points



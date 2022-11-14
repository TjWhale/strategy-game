# This file contains the world map class which is the large hex grid on which the game is played.
# It needs to be able to generate itself, draw itself and keep track of units an cities.

import pygame
import random

#this should defeinitely not be replicated here and in gui_file haha
#helper funciton for colliding points and rects
def collide_position_rect(pos, rect):
	if (pos[0] >= rect[0] and pos[0] <= rect[0] + rect[2]
		and pos[1] >= rect[1] and pos[1] <= rect[1] + rect[3]):
			return True
	return False

tile_plain = pygame.image.load("tiles/tile_plane.png").convert_alpha()
tile_deep_ocean = pygame.image.load("tiles/tile_deep_ocean.png").convert_alpha()
tile_shallow_ocean = pygame.image.load("tiles/tile_shallow_ocean.png").convert_alpha()
tile_desert = pygame.image.load("tiles/tile_desert.png").convert_alpha()
tile_human_grass = pygame.image.load("tiles/tile_human_grass.png").convert_alpha()

class world_map_class:
	def __init__(self, map_size):
		self.map_size = map_size
		self.tile_visual_size = [64,32] #how many pixels are the base tiles on the screen?
		self.actual_tile_image_size = [64,48] #how big are the actual tile images? 
		#They have blank space on the top above the top of the visible tile.
		self.tiles = []

		#add the tiles to an array
		for i in range(map_size[0]):
			self.tiles.append([])
			for j in range(map_size[1]):
				self.tiles[i].append(world_map_tile(i,j, self.tile_visual_size, self.actual_tile_image_size))

		self.check_tile_tags_for_clashes()

		#parameters for drawing the map
		self.origin_coordinates = [50,30]
		self.zoom_level = 1

	#given some coordinates for the center of the screen and a zoom level draw the map
	def draw(self, screen):
		for tile_line in self.tiles:
			for tile in tile_line:
				tile.draw(screen, self.origin_coordinates, self.zoom_level)

	def mouse_click(self, event):
		print("You clicked on the map")
		if event.type == pygame.MOUSEBUTTONDOWN:
			#select a tile on the map
			if event.button == 1:
				mouse_pos = pygame.mouse.get_pos()
				#go through the tiles and find out any that you clicked on
				for tile_line in self.tiles:
					for tile in tile_line:
						if (collide_position_rect(mouse_pos, [tile.x, tile.y, tile.x_size, tile.y_size])):
							#if the tiles image was clicked on check inside it to see if it the pixels were clicked
							click_pos = [0,0] #the point on the image tile which was clicked
							click_pos[0] = min(int((mouse_pos[0] - tile.x)/self.zoom_level), self.actual_tile_image_size[0]-1)
							click_pos[1] = min(int((mouse_pos[1] - tile.y)/self.zoom_level), self.actual_tile_image_size[1]-1)
							tile.check_click(click_pos)
							print(click_pos)

			#zoom the screen with the scroll wheel
			elif event.button == 4:
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
	def __init__(self, i, j, tile_visual_size, actual_tile_image_size):
		self.i = i #x coordinate of the tile in the grid
		self.j = j #y coordinate of the tile in the grid

		self.tile_visual_size = tile_visual_size #how big does the tile look on the screen in pixels?
		self.actual_tile_image_size = actual_tile_image_size #how big is the tile image?

		self.x = 0 #the current coordinates of the top left of the tile relative to scrolling and zooming
		self.y = 0
		self.x_size = 0 #the current size of the tile relative to zooming
		self.y_size = 0 

		self.tile_tags = [] #this contains a list of tags which determine what the tile is
		self.tile_tags.append(random.choice(["plain", "desert", "deep ocean", "shallow ocean", "human grass"]))

		self.image = pygame.Surface(actual_tile_image_size) #the compound image of everything on the tile

		self.selected = False #is this tile currently selected

	def draw(self, screen, origin_coordinates, zoom_level):
		#how much blank space is on the top of the tiles?
		tile_image_height_offset  = self.actual_tile_image_size[1] - self.tile_visual_size[1]
		#compute your relative top left corner
		screen_size = screen.get_size()
		self.x = (0.75*self.i*self.tile_visual_size[0] - origin_coordinates[0])*zoom_level + screen_size[0]/2
		self.y = (self.j*self.tile_visual_size[1] - origin_coordinates[1])*zoom_level + screen_size[1]/2
		#compute the current size of the image
		self.x_size = self.actual_tile_image_size[0]*zoom_level
		self.y_size = self.actual_tile_image_size[1]*zoom_level
		if self.i % 2 == 1:
			self.y += self.tile_visual_size[1]*zoom_level/2

		base_terrain = tile_plain
		if "desert" in self.tile_tags:
			base_terrain = tile_desert
		if "deep ocean" in self.tile_tags:
			base_terrain = tile_deep_ocean
		if "shallow ocean" in self.tile_tags:
			base_terrain = tile_shallow_ocean
		if "human grass" in self.tile_tags:
			base_terrain = tile_human_grass

		#draw everything onto your draw surface
		self.image = pygame.Surface(self.actual_tile_image_size).convert_alpha()
		self.image.fill((0,0,0,0))
		self.image.blit(base_terrain, (0,0))

		if self.selected:
			pygame.draw.circle(self.image, [255,0,0], self.selected, 2)

		#draw a polygon at that position
		#points = self.get_polygon_points()
		#pygame.draw.polygon(screen, [250,0,0], points, int(2))

		display_image = pygame.transform.rotozoom(self.image, 0, zoom_level)
		screen.blit(display_image, (self.x, self.y))

	def get_polygon_points(self):
		points = [[self.x + 0.25*self.tile_visual_size[0], self.y], 
				[self.x + 0.75*self.tile_visual_size[0], self.y], 
				[self.x + self.tile_visual_size[0], self.y + 0.5*self.tile_visual_size[1]], 
				[self.x + 0.75*self.tile_visual_size[0], self.y + self.tile_visual_size[1]], 
				[self.x + 0.25*self.tile_visual_size[0], self.y + self.tile_visual_size[1]], 
				[self.x, self.y + 0.5*self.tile_visual_size[1]]]

		return points

	#if the tile was clicked on as whole
	#then check the pixels of the image to see if they were clicked on
	def check_click(self, pos):
		print(self.i, self.j)
		print(self.image.get_at(pos))
		if self.image.get_at(pos) != (0,0,0,0):
			self.selected = pos



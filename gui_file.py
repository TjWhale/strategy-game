# This file contains the gui class which overlays the world map.

import pygame

end_turn_button = pygame.image.load("gui_elements/end_turn.png").convert_alpha()
tech_progress_button = pygame.image.load("gui_elements/tech_progress.png").convert_alpha()

#helper funciton for colliding points and rects
def collide_position_rect(pos, rect):
	if (pos[0] >= rect[0] and pos[0] <= rect[0] + rect[2]
		and pos[1] >= rect[1] and pos[1] <= rect[1] + rect[3]):
			return True
	return False


#this contains all the information for the map overlay gui
#there should only be one created on initialisation and then lots of elements as it's children
class gui_class:
	def __init__(self, screen_size):
		self.screen_size = screen_size
		print(screen_size)
		#add the elements to the gui
		self.elements = [gui_element("tech progress", tech_progress_button, [0,0,128,128]),
						gui_element("quantities", False, [128,0,256,32]),
						gui_element("end turn", end_turn_button, [screen_size[0] - 96, screen_size[1] - 96,96,96])]

	def draw(self, screen):
		for element in self.elements:
			element.draw(screen)

	def mouse_click(self, event):
		for element in self.elements:
			result = element.mouse_click(event)
			if result:
				return True
		return False

#each of the gui elements inherits from this class, this allows them to draw themselves and handle clicks
class gui_element:
	def __init__(self, name, image, position):
		self.name = name
		self.image = image
		self.screen_position = position

	def draw(self, screen):
		if self.image:
			screen.blit(self.image, (self.screen_position[0], self.screen_position[1]))
		else:
			pygame.draw.rect(screen, [0,0,255], self.screen_position)

	#if there is a click or hover does it collide with this element?
	def mouse_click(self, event):
		mouse_position = pygame.mouse.get_pos()
		if collide_position_rect(mouse_position, self.screen_position):
			print("You clicked on gui element", self.name)
			return True
		return False

	def mouse_hover(self, position):
		mouse_position = pygame.mouse.get_pos()
		if collide_position_rect(mouse_position, self.screen_position):
			print("You are hovering over gui element", self.name)
			return True
		return False






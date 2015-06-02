#!/usr/bin/python

import pygame

import common



class Graphics(object):
    """Handles all rendering and drawing operations for this program."""
    def __init__(self, common_inst):
        # Reference to common instance
        self.common = common_inst


    def set_display(self, w_width=100, w_height=100):
        """Sets up the display window, or resizes it if it is already setup."""
        # Start/Resize the display window
        pygame.display.set_mode((w_width,w_height))


    def render_disp(self):
        """Renders the display elements."""
        # Render map preview #
        # Determine tile size and window/map dimensions
        tile_size = 10
        width = len(self.common.tile_map[0])*tile_size  # number of tiles * size of tile
        height = len(self.common.tile_map)*tile_size
        map_preview = pygame.Surface((width, height))
        # TODO: Add drawing of individual tiles here
        # Adjust the display surface
        self.set_display(width, height)
        # Draw map preview to display
        pygame.display.get_surface().blit(map_preview, (0,0))
        # Update the display
        pygame.display.flip()


    def render_full_map(self):
        """Renders the map in full scale and with tile textures (if applicable)."""
        # Determine tile size and window dimenstions
        tile_size = 10
        width = len(self.common.tile_map[0])*tile_size  # number of tiles * size of tile
        height = len(self.common.tile_map)*tile_size
        # Adjust the display surface
        self.set_display(width, height)
        # Temporary test surface
        full_map = pygame.Surface((width, height))
        full_map.fill((0,100,0))
        return full_map
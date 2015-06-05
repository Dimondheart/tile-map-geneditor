#!/usr/bin/python
import pygame

import common



class Graphics(object):
    """Handles all rendering and drawing operations for this program."""
    # Colors for each tile on the minimap
    tile_colors = {
    "water" : (28,107,160),
    "sand" : (239,221,111),
    "mountainhigh" : (100,100,100),
    "forest" : (0,64,35),
    "grass" : (1,142,14),
    "none" : (0,0,0)
    }


    def __init__(self, common_inst):
        # Reference to common instance
        self.common = common_inst
        # Setup display
        pygame.display.set_caption("Tile Map GenEditor")


    def render_display(self):
        """Renders the display window elements."""
        # Render map preview #
        # Determine tile size and window/map dimensions
        tile_size = 10
        width = len(self.common.tile_map[0])*tile_size  # number of tiles * size of tile
        height = len(self.common.tile_map)*tile_size
        map_preview = pygame.Surface((width, height))
        # Draw the tiles to the surface #
        for y,row in enumerate(self.common.tile_map):
            for x,tile in enumerate(row):
                pygame.draw.rect(map_preview, self.tile_colors[tile],
                                (x*tile_size,y*tile_size,tile_size,tile_size))
        # Adjust the display surface
        pygame.display.set_mode((width,height))
        # Draw map preview to display
        pygame.display.get_surface().blit(map_preview, (0,0))
        # Update the display
        pygame.display.flip()


    def render_full_map(self):
        """Renders the map in full scale and with tile textures (if applicable)."""
        # Tile size
        tile_size = 90
        width = len(self.common.tile_map[0])*tile_size  # number of tiles * size of tile
        height = len(self.common.tile_map)*tile_size
        # Create the surface to draw to
        full_map = pygame.Surface((width, height))
        # Draw the tiles to the surface
        for y,row in enumerate(self.common.tile_map):
            for x,tile in enumerate(row):
                pygame.draw.rect(full_map, self.tile_colors[tile], (x*tile_size,y*tile_size,tile_size,tile_size))
        return full_map
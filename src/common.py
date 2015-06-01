#!/usr/bin/python

class Common(object):
    """
    Class of variables, objects, etc. that are used by multiple classes.
    Should be passed in as a reference to any new object in case it is needed.
    """
    # Root folder of this program
    root_dir = None
    # Folder of saved map data
    saved_maps_dir = None
    # Controls the edit phase of the main class
    edit_phase = False
    # 2D list of all tiles
    tile_map = []
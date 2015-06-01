#!/usr/bin/python
import sys
import os

import pygame

from lib import easygui
import common
import genmap



class Main(object):
    """Contains the core functions that manage the flow of the program."""
    def __init__(self):
        # Initialize the pygame library
        pygame.init()
        # Initialize the object used for data used by multiple objects
        self.common = common.Common()
        # Create an instance of the event handler
        self.EventHandler = Events(self.common)
        # Determine the root directory of the program
        self.common.root_dir = os.path.dirname(os.path.dirname(__file__))
        self.common.saved_maps_dir = os.path.join(self.common.root_dir, "savedmaps")
        # Create the saved maps directory if needed
        if not os.path.exists(self.common.saved_maps_dir):
            try:
                os.mkdir(self.common.saved_maps_dir)
            except Exception:
                self.EventHandler.FatalError("An error has occurred while trying to create the 'savedmaps' folder.")


    def start(self):
        """Runs whenever the program is first started/reset."""
        while True:
            # Ask if the user wants to load a map or create a new one
            prompt = "Do you want to create a new map or edit an existing one?"
            title = "Geneditor Startup"
            options = ("New Map", "Load Map","Quit")
            decision = easygui.buttonbox(prompt, title, options)
            # User wants to make a new map
            if decision == options[0]:
                self.EventHandler.new_map()
            # User wants to load a map
            elif decision == options[1]:
                self.EventHandler.load_map()
            # Quit button
            elif decision == options[2]:
                self.EventHandler.quit()
            # Quit if response is not one of the options (user canceled, etc.)
            else:
                self.EventHandler.quit()
            # Go to the edit phase, or continue to prompt the user
            if self.common.edit_phase:
                self.edit()
                break


    def edit(self):
        """The phase of generation where the user can see the map and
        tweak the results.
        """
        while self.common.edit_phase:
            self.EventHandler.do_pygame_events()
        # Terminate the program
        self.EventHandler.quit()



class Events(object):
    """Handles some generic actions as well as pygame library events."""
    # Pygame Event Reference #
        # QUIT             none
        # ACTIVEEVENT      gain, state
        # KEYDOWN          unicode, key, mod
        # KEYUP            key, mod
        # MOUSEMOTION      pos, rel, buttons
        # MOUSEBUTTONUP    pos, button
        # MOUSEBUTTONDOWN  pos, button
        # JOYAXISMOTION    joy, axis, value
        # JOYBALLMOTION    joy, ball, rel
        # JOYHATMOTION     joy, hat, value
        # JOYBUTTONUP      joy, button
        # JOYBUTTONDOWN    joy, button
        # VIDEORESIZE      size, w, h
        # VIDEOEXPOSE      none
        # USEREVENT        code
    def __init__(self, common_inst):
        # Local reference to instance of shared class
        self.common = common_inst
        # Block certain events from cluttering up the event queue
        events_to_block = [pygame.JOYAXISMOTION, pygame.JOYBALLMOTION,
                            pygame.JOYHATMOTION, pygame.JOYBUTTONUP, pygame.JOYBUTTONDOWN]
        pygame.event.set_blocked(events_to_block)


    def new_map(self):
        """Steps completed at startup when user wants to make a new map.
        Map generator instance is created after asking the user map width, height, etc.
        """
        # User input fields
        info = "These settings can be adjusted later."
        title = "Map Generator Setup"
        fields = ["Map Name", "Width", "Height", "Seed"]
        defaults = ["Default", 10, 10, "123abc"]
        values = easygui.multenterbox(info, title, fields, defaults)
        # Dict of stuff initialized in the map gen object
        param = {
        'name' : str(values[0]),
        'width' : int(values[1]),
        'height' : int(values[2]),
        'seed': str(values[3])
        }
        # Create map generator object
        self.MapGen = genmap.MapGenerator(self.common, param)
        # Generate map
        self.MapGen.gen_map()
        self.common.edit_phase = True


    def load_map(self):
        self.unimplemented_feature()
        self.common.edit_phase = False


    def save_map(self):
        self.unimplemented_feature()


    def do_pygame_events(self):
        """Processes events from the pygame event queue."""
        # Get a list of events, the first one allows the program to idle when not in use
        events = [pygame.event.wait()] + pygame.event.get()
        for event in events:
            # Quit program event (e.g. close window, etc.)
            if event.type == pygame.QUIT:
                self.common.edit_phase = False
                break
            elif event.type == pygame.MOUSEBUTTONUP:
                pass


    def unimplemented_feature(self):
        """Indicates to the user that a feature they tried to use hasn't been
        implemented yet.
        """
        # Display message box
        easygui.msgbox("That Feature is not yet available.", "Sorry!")


    def FatalError(self, msg=""):
        """Used to terminate the program with a message when a serious issue occurs.
        This includes file/directory permission issues, etc.
        """
        print msg
        # Display message
        easygui.msgbox(str(msg)+"  The program will now be terminated.",
            "A Fatal Error Has Occurred")
        self.quit()


    def quit(self):
        """Does any cleanup operations then terminates the program."""
        # Terminate pygame functions
        pygame.quit()
        sys.exit()



M = Main()
M.start()
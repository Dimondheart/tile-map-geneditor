#!/usr/bin/python
import sys
import os

import pygame

from lib import easygui
import common
import genmap
import graphics



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
                self.EventHandler.FatalExternalError("An error has occurred while trying to create the 'savedmaps' folder.")


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
            # Update the display window
            self.EventHandler.disp_update()
            # Do pygame queue events
            self.EventHandler.do_pygame_events()
        # Terminate the program
        self.EventHandler.quit()



class Events(object):
    gen_fields = ["Map Name", "Width", "Height", "Seed"]
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
        # Create graphics handling object
        self.GFX = graphics.Graphics(self.common)
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
        defaults = ["Default", 10, 10, "123abc"]
        values = easygui.multenterbox(info, title, self.gen_fields, defaults)
        # Dict of stuff initialized in the map gen object
        params = self.gen_param_to_dict(values)
        # Create map generator object
        self.MapGen = genmap.MapGenerator(self.common, params)
        # Generate map
        self.MapGen.gen_map()
        self.common.edit_phase = True


    def regen_map(self):
        """Asks the user for new generation values (eg width) then regenerates
        the map.
        """
        info = "Change any parameters to desired values."
        title = "Map Regeneration"
        # Set default field values to current map values
        defaults = [self.MapGen.name, self.MapGen.width, self.MapGen.height, self.MapGen.seed]
        # Prompt user for new generator parameters
        values = easygui.multenterbox(info, title, self.gen_fields, defaults)
        # Change values into dictionary
        params = self.gen_param_to_dict(values)
        # Now change the values in the generator object
        # TODO: Compare values to see if map regeneration is needed.
        self.MapGen.set_params(params)
        # Regenerate the map with new values
        self.MapGen.gen_map()


    def gen_param_to_dict(self, values):
        """Converts values from easygui fields list into a dictionary for the map generator."""
        # Creat dict and make sure values are the correct type
        params = {
        'name' : str(values[0]),
        'width' : int(values[1]),
        'height' : int(values[2]),
        'seed': str(values[3])
        }
        return params


    def load_map(self):
        self.unimplemented_feature()
        self.common.edit_phase = False


    def save_map(self):
        print "HI"
        """Writes the map data to a text file and image file."""
        # Prompt for the save location
        save_loc = easygui.diropenbox()
        # Make the folder to save to if necessary
        if not os.path.exists(save_loc):
            try:
                os.mkdir(save_loc)
            except Exception:
                easygui.msgbox("There was an error while trying to save the map to \n" + str(save_loc), "Map Not Saved")
                return
        # Renders the map and returns a surface
        img = self.GFX.render_full_map()
        # TODO: only allow letters, numbers and certain characters in the file name
        img_file = os.path.join(save_loc, self.MapGen.name + ".bmp")
        # Check if that is already a file(s) with that name(s), and if it ok to override it
        msg = "\"" + self.MapGen.name + ".bmp \" already exists.  Override?"
        options = ("Yes", "No")
        if os.path.exists(img_file) and not easygui.buttonbox(msg, "Continue?", options) == "Yes":
            return
        else:
            pygame.image.save(img, img_file)
            easygui.msgbox("\"" + self.MapGen.name + "\" saved successfully", "Save Complete")


    def do_pygame_events(self):
        """Processes events from the pygame event queue."""
        # Get a list of events, the first one allows the program to idle when not in use
        events = [pygame.event.wait()] + pygame.event.get()
        for event in events:
            print event
            # Quit program event (e.g. close window, etc.)
            if event.type == pygame.QUIT:
                self.common.edit_phase = False
                break
            # Event processing for during the edit phase
            elif self.common.edit_phase:
                self.do_pygame_edit_phase_event(event)
            # Other situations
            else:
                pass


    def do_pygame_edit_phase_event(self, event):
        """Processes reactions to pygame events for the edit phase."""
        print "HIHIHI"
        # Keyboard release
        if event.type == pygame.KEYUP:
            # 'R' key; modify generation settings then regenerate
            if event.key == pygame.K_r:
                self.regen_map()
        # Keyboard press
        elif event.type == pygame.KEYDOWN:
            # Save the current map (CTRL+S)
            if event.key == pygame.K_s and (
            pygame.key.get_pressed()[pygame.K_LCTRL] or pygame.key.get_pressed()[pygame.K_RCTRL]):
                self.save_map()


    def disp_update(self):
        """Updates the display window."""
        self.GFX.render_disp()


    def unimplemented_feature(self):
        """Indicates to the user that a feature they tried to use hasn't been
        implemented yet.
        """
        # Display message box
        easygui.msgbox("That Feature is not yet available.", "Sorry!")


    def FatalExternalError(self, msg=""):
        """Used to terminate the program with a message when a serious issue occurs.
        This includes file/directory permission issues, etc.
        """
        print msg
        # Display message
        easygui.msgbox(str(msg)+"  The program will now be terminated.",
            "A Fatal External Error Has Occurred")
        self.quit()


    def quit(self):
        """Does any cleanup operations then terminates the program."""
        # Terminate pygame functions
        pygame.quit()
        sys.exit()



M = Main()
M.start()
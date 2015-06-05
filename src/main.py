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
            self.EventHandler.update_display()
            # Do pygame queue events
            self.EventHandler.do_pygame_events()
        # Terminate the program
        self.EventHandler.quit()



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
class Events(object):
    """Handles some generic actions as well as pygame library events."""
    # Fields for the input box for the generator
    gen_fields = ["Width", "Height", "Seed"]


    def __init__(self, common_inst):
        # Local reference to shared data object instance
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
        # Parts of the prompt window
        info = "These settings can be adjusted later."
        title = "Map Generator Setup"
        # Get map generation parameters
        params = self.gen_param_prompt(info, title, self.gen_fields)
        # Create map generator object
        self.MapGen = genmap.MapGenerator(self.common, params)
        # Generate map
        self.MapGen.gen_map()
        # Tells main to go into the edit phase
        self.common.edit_phase = True


    def regen_map(self):
        """Asks the user for new generation values (eg width) then regenerates
        the map.
        """
        # Parts of the prompt window
        info = "Change any parameters to desired values."
        title = "Map Regeneration"
        # Set default field values to current map values
        defaults = [self.MapGen.width, self.MapGen.height, self.MapGen.seed]
        # Get generation parameters
        params = self.gen_param_prompt(info, title, self.gen_fields, defaults)
        # Now change the values in the generator object
        # TODO: Compare values to see if map regeneration is needed.
        self.MapGen.set_params(params)
        # Regenerate the map with new values
        self.MapGen.gen_map()


    def gen_param_prompt(self, msg="Fill in fields", title="Prompt", fields=[], defaults=[]):
        """Prompts the user to enter various map generation parameters, and returns
        them as a dictionary.
        """
        # Prompt uer for data
        values = easygui.multenterbox(msg, title, fields, defaults)
        # Creat dictionary, make sure types match
        params = {
        'width' : int(values[0]),
        'height' : int(values[1]),
        'seed': values[2]
        }
        return params


    def load_map(self):
        self.unimplemented_feature()
        self.common.edit_phase = False


    def save_map(self):
        """Writes the map data to a text file and image file."""
        # Prompt for the save location
        save_path = easygui.filesavebox("Two files will be created, one image and one text file.")
        # Renders the map and returns a surface
        img = self.GFX.render_full_map()
        # Check if that is already a file(s) with that name(s), and if it ok to override it
        msg = "There is already a file in this location with that name.  Override?"
        if (os.path.exists(save_path + ".bmp") or os.path.exists(save_path + ".txt")) and easygui.buttonbox(msg, "Continue?", ("Yes", "No")) == "No":
            return
        else:
            # Save image to file
            pygame.image.save(img, save_path + ".bmp")
            # Indicate saving is complete
            easygui.msgbox("\"" + str(os.path.basename(save_path)) + "\" saved successfully", "Save Complete")


    def do_pygame_events(self):
        """Processes events from the pygame event queue."""
        # Get a list of events, the first one allows the program to idle when not in use
        events = [pygame.event.wait()] + pygame.event.get()
        for event in events:
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
        # Keyboard release
        if event.type == pygame.KEYUP:
            # 'R' key; modify generation settings then regenerate
            if event.key == pygame.K_g:
                self.regen_map()
        # Keyboard press
        elif event.type == pygame.KEYDOWN:
            # Save the current map (CTRL+S)
            if event.key == pygame.K_s and (
            pygame.key.get_pressed()[pygame.K_LCTRL] or pygame.key.get_pressed()[pygame.K_RCTRL]):
                self.save_map()


    def update_display(self):
        """Updates the display window."""
        self.GFX.render_display()


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
## 0.5.1 Alpha (Current)

####Bug Fixes
- Fixed crash due to canceling the new map window when in edit/preview mode

####Miscellaneous
- Main menu displays a 'Close Menu' button instead of 'Quit' when there is an open map
- Made a simple shell script for Linux (you will have to manually mark it as executable for now)


## 0.5 Alpha

####New Features
- Menu displayed on start up is now the main menu (access by pressing 'Escape' key)

####Optimizations
- Integrated map regeneration into the main menu (just use the 'new map' button)


## 0.4 Alpha

####New Features
- Maps are now saved as both an image (bitmap) and text file (JSON data)
- Maps can now be loaded from a text file

####Optimizations
- Greatly sped up map generation time

####Bug Fixes
- The same seed and map dimensions will always generate the same map
- Random seed selection fixed
- Fixed crashes that occurred when the user canceled a file open/close window or text prompt window

####Miscellaneous
- Minor improvements to indicator/prompt windows


## 0.3 Alpha

####New Features
- Preview of map
- Rendering and saving the map as an image
- Random seed option
	- Leave seed box blank

####Optimizations
- Optimized map generation
	- For Example name is not a parameter
- Saving uses the file save interface instead of open directory

####Miscellaneous
- "README.md" - added sample map image and link to "CHANGELOG.md"
- Changed regenerate keyboard key from 'r' to 'g'


## 0.2 Alpha

####New Features
- Changing of basic generator parameters (width, seed, etc.) and map regeneration after initial startup (press 'R' in edit phase)
- Saving of map images (only creates a test image until graphics are implemented)
- Started implementing graphics and rendering of the map

####Optimizations
- Optimized Pygame event handling

####Bug Fixes
- Minor bugfixes
- Note: There is a weird bug right now that causes keys to act strange for me, you may have to press CTRL+S a couple times at the same time to get the save window to pop up

####Miscellaneous
- Code cleanup & organization
- More confirmation/notification indicator windows

####Non-Code
- README.md updated


## 0.1 Alpha

####New Features
- Implemented many core features
	- Code structure
	- Map generation
	- Miscellaneous interface components

####Miscellaneous
- Important miscellaneous files (like start/run files)
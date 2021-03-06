#GenEditor for Tile Maps#
**Note: See [CHANGELOG.md](CHANGELOG.md) for detailed version logs.**  

![tile_map_geneditor_sample](https://cloud.githubusercontent.com/assets/7505459/8014902/232b571e-0b9a-11e5-954c-ed1159d38334.png)  

This is a tool for generating and editing grid/tile-based maps.


##Features##

###Current Features###
- Generates a tile map from a user-specified width, height, and random number generator seed
	- Uses the Perlin noise generator method
- Display a small preview of the generated map
- Change one or more values like width, height, and seed after generation then regenerate
- Save a map as a text file and image file
- Load a map from a text file

###Planned Features###
- Post-generation tweaking of a map (manual tile editing, etc.)
- Custom tile textures
	- Support for different ways textures can be stored (like large texture map files, etc.)
- And more

###Possible Future Features###
- Interface for modifying core generation components like water level, occurrence rate of biomes, etc.
- Display a full-scale, custom textures included, rendering of the map before saving
- Improved tile map generator (smoother, easier to manipulate, better biome handling, etc)
- Customizing how the map data is saved and what data is included (like tile type and biome)
- Optional grid lines in image
- Isomeric map rendering
- And more


##License##
The MIT License (MIT)

Copyright (c) 2015 Bryan Charles Bettis

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
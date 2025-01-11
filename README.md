# cube_3d_render
Adds an App class which takes in lists of coordinates and generates a window rendering cubes at the specified coordinates using OpenGL and pygame

## Installation

To use the module, either download it to your project folder or install it by running `pip install git+https://github.com/Remy-Pa/cube_3d_render.git`

## Use

To render the cubes in 3d, simply pass in a list of coordinates and a list of colors (optional) when initializing the App class.

For example, these coordinates draw a smiling face. The third color was chosen randomly since there were 3 nested tuples of coordinates but only 2 for colors.

```python
import cube_3d_render

coordinates = (
        ((110,110,50), (111,110,50), (110,111,50), (111,111,50), (120, 110, 50), (121, 110, 50), (120, 111, 50), (121, 111, 50)),
        ((115,100,55), (114,99,55), (116,99,55)),
        ((110,80, 52), (112,78,52), (114,76,52), (116,76,52), (118,78,52), (120,80,52)),
)

colors = [(0,0,1), (1,1,0)]

cube_3d_render.App(coords_lists = coordinates, colors_list = colors)
```

### Output

The above code outputs this. The model can be rotated and moved closer by using the keyboard arrow keys.

![image](https://github.com/user-attachments/assets/3bf70770-8a46-4898-a93b-0f23cafe9204)
![image](https://github.com/user-attachments/assets/08b0be77-a613-4a1c-b691-3caa27f5d427)


## Detailed description

### App
Generates a window where the specified cubes are rendered. It is possible to zoom and rotate the image using the keyboard arrow keys (`&larr;`, `&uarr;`, `&darr;` and `&rarr;`).

> **cube_3d_render.App(**coords_lists = [], colors_list = [], win_size = (1728, 972), background_color = (0.1,0.1,0.1)**)**

* coords_lists : list or tuple of nested lists or tuples containing xyz coordinates of each cube to render
* colors_list : list of nested lists or tuples containing RGB values for the color in which to render each group of cube. If the colors_list length does not match coords_lists, random colors will be added.
* win_size : list or tuple of the size of the window of the application
* background_color : list or tuple of the color to be used as the background

### Cube
Generates a cube object holding vertices and normals.
> **cube_3d_render.Cube(**coords = (0,0,0)**)**

* coords : list or tuple of the xyz coordinates at which to render the cube. Passing lists to the cube_3d_render.App object should be prefered since it renders the cubes using a display list and is more efficient.


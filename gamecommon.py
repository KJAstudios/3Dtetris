# Game Common to store all global variables
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

## List of possible tetris block shapes
# Used for checking if shape is valid or for randomly getting shapes
shapeList = ['box','S','L','straight','T']

## List of existing blocks
blockList = []

# 3 positions, 3 colors, 3 normals, 2 UVs
#verts = np.float32([(1, -1, -1, color[0], color[1], color[2], 0, 0, -1, 0, 0),
#                            (1, 1, -1, color[0], color[1], color[2], 0, 0, -1, 1, 0),
#                            (-1, 1, -1, color[0], color[1], color[2], 0, 0, -1, 1, 1),
#                            (-1, -1, -1, color[0], color[1], color[2], 0, 0, -1, 0, 1),

#                            (-1, -1, -1, color[0], color[1], color[2], -1, 0, 0, 0, 0),
#                            (-1, 1, -1, color[0], color[1], color[2], -1, 0, 0, 1, 0),
#                            (-1, 1, 1, color[0], color[1], color[2], -1, 0, 0, 1, 1),
#                            (-1, -1, 1, color[0], color[1], color[2], -1, 0, 0, 0, 1),

#                            (-1, -1, 1, color[0], color[1], color[2], 0, 0, 1, 0, 0),
#                            (-1, 1, 1, color[0], color[1], color[2], 0, 0, 1, 1, 0),
#                            (1, 1, 1, color[0], color[1], color[2], 0, 0, 1, 1, 1),
#                            (1, -1, 1, color[0], color[1], color[2], 0, 0, 1, 0, 1),
                                  
#                            (1, -1, 1, color[0], color[1], color[2], 1, 0, 0, 0, 0),
#                            (1, 1, 1, color[0], color[1], color[2], 1, 0, 0, 1, 0),
#                            (1, 1, -1, color[0], color[1], color[2], 1, 0, 0, 1, 1),
#                            (1, -1, -1, color[0], color[1], color[2], 1, 0, 0, 0, 1),
                                  
#                            (1, 1, -1, color[0], color[1], color[2], 0, 1, 0, 0, 0),
#                            (1, 1, 1, color[0], color[1], color[2], 0, 1, 0, 1, 0),
#                            (-1, 1, 1, color[0], color[1], color[2], 0, 1, 0, 1, 1),
#                            (-1, 1, -1, color[0], color[1], color[2], 0, 1, 0, 0, 1),
                                  
#                            (1, -1, 1, color[0], color[1], color[2], 0, -1, 0, 0, 0),
#                            (1, -1, -1, color[0], color[1], color[2], 0, -1, 0, 1, 0),
#                            (-1, -1, -1, color[0], color[1], color[2], 0, -1, 0, 1, 1),
#                            (-1, -1, 1, color[0], color[1], color[2], 0, -1, 0, 0, 1)
#                            ])

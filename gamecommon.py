# Game Common to store all global variables
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

## List of possible tetris block shapes
# Used for checking if shape is valid or for randomly getting shapes
shapeList = ['box', 'S', 'L', 'straight', 'T']

## Dictionary of vertices per type

shapeCornerDict = {'box': [(0, 0, 0), (1, 0, 0),
                           (1, 1, 0), (0, 1, 0),

                           (0, 0, -1), (1, 0, -1),
                           (1, 1, -1), (0, 1, -1)],

                   'S': [(0, 0, 0), (0, 1, 0),
                                    (0, 1, -1), (0, 2, -1)],

                   'L': [(0, 0, 0),
                         (0, 0, -1),
                         (0, 0, -2), (0, 1, -2)],

                   'straight': [(0, 0, 0),
                                (0, 0, -1),
                                (0, 0, -2),
                                (0, 0, -3)],

                   'T': [(0, 0, 0), (0, 1, 0), (0, 2, 0),
                                    (0, 1, -1)]}

## List of existing blocks
blockList = []

## Id count for numbering the blocks
blockID = [1]

## New Block indicator
# 1 if new block should be summoned 
# 0 if not
newBlock = [0]

### Game Grid
# 3D numpy array 8 x 8 x 10, zero means empty, other numbers refer to block id

gameGrid = np.zeros((8, 8, 10))

# Example:
# gameGrid = [[[0,0,0,0,0,0,0,2],
             # [0,0,0,0,0,0,0,2],
             # [0,1,1,0,0,0,0,2],
             # [0,1,1,0,0,0,0,2],
             # [0,0,0,0,0,0,0,0],
             # [0,0,0,0,0,0,0,0],
             # [0,0,0,0,0,0,0,0],
             # [0,0,0,0,0,0,0,0]],

             #[[0,0,0,0,0,0,0,3],
             # [0,1,1,0,0,0,0,3],
             # [0,1,1,0,0,0,0,3],
             # [0,0,0,0,0,0,0,0],
             # [0,0,0,0,0,0,0,0],
             # [0,0,0,0,0,0,0,0],
             # [0,0,0,0,0,0,0,0],
             # [0,0,0,0,0,0,0,0]],

             #[[0,4,0,0,0,0,0,3],
             # [0,4,4,0,0,0,0,0],
             # [0,4,0,0,0,0,0,0],
             # [0,0,0,0,0,0,0,0],
             # [0,0,0,0,0,0,0,0],
             # [0,0,0,0,0,0,0,0],
             # [0,0,0,0,0,0,0,0],
             # [0,0,0,0,0,0,0,0]]]

# In this case there are only 3 rows for space's sake, normally there would be 10
# 1 is a cube
# 2 is a straight
# 3 is an L
# and 4 is a T

###


#
#
#
#
#
#
#





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

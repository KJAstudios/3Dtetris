from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math
from obj_loader_2 import LoadOBJ
from gamecommon import shapeList

_lightVector = np.asfarray([0, 0, 1])

class SlowCube:
    def __init__(self,id,type=None,rotateSpeed=50.0):
        global shapeList

        # Get type of shape
        self.type = type

        # Set id
        self.id = id

        # Check if shape type is valid
        if self.type in shapeList:
            model = LoadOBJ(f"resources/models/{self.type}_tetris_piece.obj")
        else:
            print('Major Error! Shape type not recognized!')
            # Would be good to enter code to delete 'self' if this occurs
            return False

        self.verts = np.asfarray(model["verts"])
        self.surfaces = np.asarray(model["surfs"])
        self.normals = np.asfarray(model["normals"])

        # color of the shape
        # TODO change this to texture wrapping
        self.color = np.asfarray([0, 0, 1])

        # Starting Angle
        self.ang = 0
        # Get speed of rotation
        self.rotateSpeed = rotateSpeed
        # Axis of rotation
        self.axis = (3, 1, 1)

    def Update(self, deltaTime,currentID):
        if self.id == currentID:
            # Update Angle if current Shape
            self.ang += self.rotateSpeed * deltaTime

    def DrawBlock(self):
        global _lightVector

        invT = np.linalg.inv(glGetDouble(GL_MODELVIEW_MATRIX)).transpose()
        glBegin(GL_QUADS)
        for n, surface in enumerate(self.surfaces):
            for vert in surface:
                norm = np.append(self.normals[vert[1]], 1)
                modelNorm = np.matmul(norm, invT)
                modelNorm = np.delete(modelNorm, 3)
                np.linalg.norm(modelNorm)

                dotP = np.dot(_lightVector, modelNorm)
                mult = max(min(dotP, 1), 0)
                glColor3fv(self.color * mult)

                glVertex3fv(self.verts[vert[0]])
        glEnd()

    def Render(self):
        m = glGetDouble(GL_MODELVIEW_MATRIX)

        glRotatef(self.ang, *self.axis)

        self.DrawBlock()

        glLoadMatrixf(m)

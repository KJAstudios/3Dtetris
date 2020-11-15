from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math
from obj_loader import LoadOBJ

_lightVector = np.asfarray([0, 0, 1])


class SlowCube:
    def __init__(self):
        model = LoadOBJ("resources/models/S_tetris_piece.obj")

        self.verts = model["verts"]
        self.surfaces = model["surfs"]
        self.normals = model["normals"]

        # color of the shape
        # TODO change this to texture wrapping
        self.color = np.asfarray([0, 0, 1])

        self.ang = 0
        self.axis = (3, 1, 1)

    def Update(self, deltaTime):
        self.ang += 50.0 * deltaTime

    def DrawBlock(self):
        global _lightVector

        invT = np.linalg.inv(glGetDouble(GL_MODELVIEW_MATRIX)).transpose()
        glBegin(GL_QUADS)
        for n, surface in enumerate(self.surfaces):
            for vert in surface:
                norm = np.append(self.normals[n], 1)
                modelNorm = np.matmul(norm, invT)
                modelNorm = np.delete(modelNorm, 3)
                np.linalg.norm(modelNorm)

                dotP = np.dot(_lightVector, modelNorm)
                mult = max(min(dotP, 1), 0)
                glColor3fv(self.color * mult)

                glVertex3fv(self.verts[vert])
        glEnd()

    def Render(self):
        m = glGetDouble(GL_MODELVIEW_MATRIX)

        glRotatef(self.ang, *self.axis)

        self.DrawBlock()

        glLoadMatrixf(m)

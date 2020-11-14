from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math
from obj_loader import LoadOBJ

_lightVector = np.asfarray([0, 0, 1])


class SlowCube:
    def __init__(self):
        model = LoadOBJ("resources/models/box_tetris_piece.obj")
        # vertices of the 3D model
        # self.verts = np.asfarray([(1, -1, -1),
        #                          (1, 1, -1),
        #                          (-1, 1, -1),
        #                          (-1, -1, -1),
        #                         (1, -1, 1),
        #                          (1, 1, 1),
        #                          (-1, -1, 1),
        #                          (-1, 1, 1)])

        self.verts = model["verts"]

        # Vertices that make a face of the model
        # self.surfaces = np.array([(0, 1, 2, 3),
        #                          (3, 2, 7, 6),
        #                          (6, 7, 5, 4),
        #                          (4, 5, 1, 0),
        #                          (1, 5, 7, 2),
        #                          (4, 0, 3, 6)])

        self.surfaces = model["surfs"]

        # color of the shape
        # TODO change this to texture wrapping
        self.color = np.asfarray([0, 0, 1])

        # the vertex normals, don't know why this is smaller than the number of vertices
        # self.normals = np.asfarray([(0, 0, -1),
        #                            (-1, 0, 0),
        #                            (0, 0, 1),
        #                            (1, 0, 0),
        #                            (0, 1, 0),
        #                            (0, -1, 0)])

        self.normals = model["normals"]

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

                glVertex3fv(self.verts[vert-1])
        glEnd()

    def Render(self):
        m = glGetDouble(GL_MODELVIEW_MATRIX)

        glRotatef(self.ang, *self.axis)

        self.DrawBlock()

        glLoadMatrixf(m)

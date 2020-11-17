from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
import numpy as np
import math
from obj_loader_2 import LoadOBJ
from gamecommon import shapeList

_lightVector = np.asfarray([0, 0, 1])

class SlowCube:
    def __init__(self,id,type=None,rotateSpeed=100.0,pos=(0,0,0)):
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

        # Set verts, surfaces, and normals
        self.verts = np.asfarray(model["verts"])
        self.surfaces = np.asarray(model["surfs"])
        self.normals = np.asfarray(model["normals"])

        # If necessary, translate based on pos
        self.pos = pos
        if self.pos != (0,0,0):
            for i in self.verts:
                i[0] += self.pos[0]
                i[1] += self.pos[1]
                i[2] += self.pos[2]

        # color of the shape
        # TODO change this to texture wrapping
        self.color = np.asfarray([0, 0, 1])

        # Starting Angle
        self.ang = 0
        # Get speed of rotation
        self.rotateSpeed = rotateSpeed
        # Axis of rotation (0,0,0) + self.pos
        self.axis = (self.pos[0],self.pos[1],self.pos[2])

    def Update(self, deltaTime,currentID):
        if self.id == currentID or currentID == -1:
            # Update Angle if current Shape
            self.ang += self.rotateSpeed * deltaTime

    def LoadTexture(self):
        # Load texture image
        try:
            textureSurf = pygame.image.load(f"resources/textures/{self.type}_tetris_texture.png")
        except:
            print('Error Loading Texture! Reverting to default color.')
            return None

        # Convert it to text
        textureText = pygame.image.tostring(textureSurf, "RGBA", 1)

        # Texture width and height
        width  = textureSurf.get_width()
        height = textureSurf.get_height()

        # Do all the crazy gl stuff
        glEnable(GL_TEXTURE_2D)
        textureID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D,textureID)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, textureText)

        return textureID

    def DrawBlock(self):
        global _lightVector
        texture = self.LoadTexture()
        invT = np.linalg.inv(glGetDouble(GL_MODELVIEW_MATRIX)).transpose()
        glBegin(GL_QUADS)
        for n, surface in enumerate(self.surfaces):
            for vert in surface:
                norm = np.append(self.normals[vert[1]], 1)
                modelNorm = np.matmul(norm, invT)
                modelNorm = np.delete(modelNorm, 3)
                np.linalg.norm(modelNorm)

                #

                #if texture == None:
                dotP = np.dot(_lightVector, modelNorm)
                mult = max(min(dotP, 1), 0)
                glColor3fv(self.color * mult)
                #else:
                #    glEnable(GL_TEXTURE_3D)
                #    glBindTexture(GL_TEXTURE_2D, texture)

                glVertex3fv(self.verts[vert[0]])
        glEnd()

    def Render(self):
        m = glGetDouble(GL_MODELVIEW_MATRIX)

        glRotatef(self.ang, *self.axis)

        self.DrawBlock()

        glLoadMatrixf(m)

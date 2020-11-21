
import pygame
import numpy as np
import math
from obj_to_vbo import LoadOBJ
from gamecommon import *
from PIL import Image

_lightVector = np.asfarray([0, 0, 1])  # <- Unused _lightvector

from OpenGL.arrays import vbo
from OpenGL.GL import shaders


class Cube:
    def __init__(self, id, type=None, rotateSpeed=100.0, pos=(0, 0, 0)):
        global shapeList

        # color of the shape
        # TODO change this to texture wrapping
        self.color = np.asfarray([1, 1, 1])
        color = np.asfarray([1, 1, 1])

        # Get type of shape
        self.type = type

        # Set id
        self.id = id
        self.model_size = 0

        # Check if shape type is valid
        if self.type in shapeList:
            model = LoadOBJ(f"resources/models/{self.type}_tetris_piece.obj", self.color)
            self.model_size = len(model)
        else:
            print('Major Error! Shape type not recognized!')
            # Would be good to enter code to delete 'self' if this occurs
            return False

        ################################################
        ### NEED TO CHANGE IN ORDER FOR GAME TO WORK ###
        ################################################

        # Set verts, surfaces, and normals
        # self.vertsTemp = np.asfarray(model["verts"])
        # self.surfaces = np.asarray(model["surfs"])
        # self.normals = np.asfarray(model["normals"])
        ###

        #######################
        ### NEED self.verts ###
        #######################

        # For now just use default cube until obj loader is fixed. Use this cube to test texture/ui
        # 3 positions, 3 colors, 3 normals, 2 UVs
        '''
        self.verts = np.float32([(1, -1, -1, color[0], color[1], color[2], 0, 0, -1, 0, 0),
                                 (1, 1, -1, color[0], color[1], color[2], 0, 0, -1, 1, 0),
                                 (-1, 1, -1, color[0], color[1], color[2], 0, 0, -1, 1, 1),
                                 (-1, -1, -1, color[0], color[1], color[2], 0, 0, -1, 0, 1),

                                 (-1, -1, -1, color[0], color[1], color[2], -1, 0, 0, 0, 0),
                                 (-1, 1, -1, color[0], color[1], color[2], -1, 0, 0, 1, 0),
                                 (-1, 1, 1, color[0], color[1], color[2], -1, 0, 0, 1, 1),
                                 (-1, -1, 1, color[0], color[1], color[2], -1, 0, 0, 0, 1),

                                 (-1, -1, 1, color[0], color[1], color[2], 0, 0, 1, 0, 0),
                                 (-1, 1, 1, color[0], color[1], color[2], 0, 0, 1, 1, 0),
                                 (1, 1, 1, color[0], color[1], color[2], 0, 0, 1, 1, 1),
                                 (1, -1, 1, color[0], color[1], color[2], 0, 0, 1, 0, 1),

                                 (1, -1, 1, color[0], color[1], color[2], 1, 0, 0, 0, 0),
                                 (1, 1, 1, color[0], color[1], color[2], 1, 0, 0, 1, 0),
                                 (1, 1, -1, color[0], color[1], color[2], 1, 0, 0, 1, 1),
                                 (1, -1, -1, color[0], color[1], color[2], 1, 0, 0, 0, 1),

                                 (1, 1, -1, color[0], color[1], color[2], 0, 1, 0, 0, 0),
                                 (1, 1, 1, color[0], color[1], color[2], 0, 1, 0, 1, 0),
                                 (-1, 1, 1, color[0], color[1], color[2], 0, 1, 0, 1, 1),
                                 (-1, 1, -1, color[0], color[1], color[2], 0, 1, 0, 0, 1),

                                 (1, -1, 1, color[0], color[1], color[2], 0, -1, 0, 0, 0),
                                 (1, -1, -1, color[0], color[1], color[2], 0, -1, 0, 1, 0),
                                 (-1, -1, -1, color[0], color[1], color[2], 0, -1, 0, 1, 1),
                                 (-1, -1, 1, color[0], color[1], color[2], 0, -1, 0, 0, 1)
                                 ])'''

        self.verts = np.float32(model)
        # Vertex Shader thing?
        self.VERTEX_SHADER = shaders.compileShader("""#version 130
        uniform mat4 invT;
        attribute vec3 position;
        attribute vec3 color;
        attribute vec3 vertex_normal;
        out vec4 vertex_color;
        void main()
        {
            vec4 norm = invT * vec4(vertex_normal,1.0);
            gl_Position = gl_ModelViewProjectionMatrix * vec4(position,1.0);
            vertex_color = vec4(color * min(1, max(0, norm[2])), 1.0);
        }""", GL_VERTEX_SHADER)

        self.FRAGMENT_SHADER = shaders.compileShader("""#version 130 
        in vec4 vertex_color;
        out vec4 fragColor;
        void main()
        {
            fragColor = vertex_color;
        }""", GL_FRAGMENT_SHADER)

        self.shader = shaders.compileProgram(self.VERTEX_SHADER, self.FRAGMENT_SHADER)
        self.vbo = vbo.VBO(self.verts)  # <- this is where verts is processed

        self.uniformInvT = glGetUniformLocation(self.shader, "invT")
        self.position = glGetAttribLocation(self.shader, "position")
        self.color = glGetAttribLocation(self.shader, "color")
        self.vertex_normal = glGetAttribLocation(self.shader, "vertex_normal")

        # If necessary, translate based on pos
        self.pos = pos
        if self.pos != (0, 0, 0):
            for i in self.verts:
                i[0] += self.pos[0]
                i[1] += self.pos[1]
                i[2] += self.pos[2]

        # Starting Angle
        self.ang = 0
        # Get speed of rotation
        self.rotateSpeed = rotateSpeed
        # Axis of rotation (0,0,0) + self.pos
        self.axis = (self.pos[0], self.pos[1], self.pos[2])

        # Load texture image
        try:
            self.textureSurf = Image.open(f"resources/textures/{self.type}_tetris_texture.jpg")
        except Error as e:
            print(f'Major Error: {e}')
            return None

        self.textureData = np.array(list(self.textureSurf.getdata()), np.uint8)

        format = GL_RGB if self.textureData.shape[0] == 3 else GL_RGBA

        self.textureGen = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.textureGen)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.textureSurf.width, self.textureSurf.height, 0, GL_RGB, GL_UNSIGNED_BYTE, self.textureData)
        glEnable(GL_TEXTURE_2D)

    def Update(self, deltaTime, currentID):
        if self.id == currentID or currentID == -1:
            # Update Angle if current Shape
            self.ang += self.rotateSpeed * deltaTime

    #def LoadTexture(self):
    #    # Load texture image
    #    try:
    #        textureSurf = pygame.image.load(f"resources/textures/{self.type}_tetris_texture.png")
    #    except:
    #        print('Error Loading Texture! Reverting to default color.')
    #        return None

    #    # Convert it to text
    #    textureText = pygame.image.tostring(textureSurf, "RGBA", 1)

    #    # Texture width and height
    #    width = textureSurf.get_width()
    #    height = textureSurf.get_height()
    #    # Do all the crazy gl stuff
    #    glEnable(GL_TEXTURE_2D)
    #    textureID = glGenTextures(1)
    #    glBindTexture(GL_TEXTURE_2D, textureID)
    #    # glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    #    # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    #    # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    #    # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    #    # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    #    # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    #    # glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    #    # glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    #    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, textureText)

    #    return textureID

    def DrawBlock(self):

        
        shaders.glUseProgram(self.shader)
        invT = np.linalg.inv(glGetDouble(GL_MODELVIEW_MATRIX)).transpose()
        glUniformMatrix4fv(self.uniformInvT, 1, False, invT)
        try:
            self.vbo.bind()
            try:
                glEnableVertexAttribArray(self.position)
                glEnableVertexAttribArray(self.color)
                glEnableVertexAttribArray(self.vertex_normal)
                stride = 44
                glVertexAttribPointer(self.position, 3, GL_FLOAT, False, stride, self.vbo)
                glVertexAttribPointer(self.color, 3, GL_FLOAT, False, stride, self.vbo + 12)
                glVertexAttribPointer(self.vertex_normal, 3, GL_FLOAT, True, stride, self.vbo + 24)
                glDrawArrays(GL_QUADS, 0, self.model_size)
                
                
            finally:
                self.vbo.unbind()
                glDisableVertexAttribArray(self.position)
                glDisableVertexAttribArray(self.color)
                glDisableVertexAttribArray(self.vertex_normal)
        finally:
            shaders.glUseProgram(0)
            glClearColor(0.0, 0.0, 0.0, 1.0)
            
            
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.textureGen)
            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
            #glEnable(GL_DEPTH_TEST)
            

    def OldDrawBlock(self):

        #####################################
        ##        Old Drawing Code         ##
        #####################################

        global _lightVector

        # glEnable(GL_TEXTURE_3D)
        # texture = self.LoadTexture()
        # glBindTexture(GL_TEXTURE_2D, texture)
        # glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

        # invT = np.linalg.inv(glGetDouble(GL_MODELVIEW_MATRIX)).transpose()
        # glBegin(GL_QUADS)
        # for n, surface in enumerate(self.surfaces):
        #    for vert in surface:
        #        norm = np.append(self.normals[vert[1]], 1)
        #        modelNorm = np.matmul(norm, invT)
        #        modelNorm = np.delete(modelNorm, 3)
        #        np.linalg.norm(modelNorm)

        #        #if texture == None:
        #        dotP = np.dot(_lightVector, modelNorm)
        #        mult = max(min(dotP, 1), 0)
        #        glColor3fv(self.color * mult)

        #        glVertex3fv(self.vertsTemp[vert[0]])
        # glEnd()

        ####################################

    def Render(self):
        m = glGetDouble(GL_MODELVIEW_MATRIX)

        glRotatef(self.ang, *self.axis)

        self.DrawBlock()

        glLoadMatrixf(m)

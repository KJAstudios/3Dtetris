
import pygame
import numpy as np
import math
from obj_to_vbo import LoadOBJ
from gamecommon import *
from PIL import Image

_lightVector = np.asfarray([0, 0, 1])  # <- Unused _lightvector

from OpenGL.arrays import vbo
from OpenGL.GL import shaders

### Notes
# Cube() is the class of each cube used in the game.
# Each frame DrawBlock() is called for each cube along with Update()
# Presumably, the reason textures are not working has to do with the shaders.
# 



class Cube:
    def __init__(self, type=None, rotateSpeed=100.0, pos=(0, 0, 10)):
        global shapeList

        # color of the shape
        self.color = np.asfarray([1, 1, 1])
        color = np.asfarray([1, 1, 1])

        # Get type of shape
        self.type = type

        # Set id
        self.id = blockID[0]
        blockID[0] += 1

        self.model_size = 0

        # Check if shape type is valid
        if self.type in shapeList:
            model = LoadOBJ(f"resources/models/{self.type}_tetris_piece.obj", self.color)
            self.model_size = len(model)
        else:
            print('Major Error! Shape type not recognized!')
            self._delete()
            print('Removing Block...')


        # The array of shape properties
        self.verts = np.float32(model)

        # Vertex Shader thing?
        self.VERTEX_SHADER = shaders.compileShader("""#version 130
        uniform mat4 invT;
        attribute vec3 position;
        attribute vec3 color;
        attribute vec3 vertex_normal;
        attribute vec2 aTexCoord;
        out vec4 vertex_color;
        out vec2 TexCoord;
        void main()
        {
            vec4 norm = invT * vec4(vertex_normal,0.0);
            gl_Position = gl_ModelViewProjectionMatrix * vec4(position,1.0);
            vertex_color = vec4(color * min(1, max(0, norm[2])), 1.0);
            TexCoord = aTexCoord;
        }""", GL_VERTEX_SHADER)

        # Fragment Shader thing?
        self.FRAGMENT_SHADER = shaders.compileShader("""#version 130 
        precision highp float;

        in vec4 vertex_color;
        in vec2 TexCoord;
        out vec4 fragColor;

        uniform sampler2D texUnit; 

        void main() {
            fragColor = texture(texUnit, TexCoord);
        }""", GL_FRAGMENT_SHADER)

        # Compile Shader
        self.shader = shaders.compileProgram(self.VERTEX_SHADER, self.FRAGMENT_SHADER)
        
        # Core OpenGL requires that at least one OpenGL vertex array be bound
        VAO = glGenVertexArrays(1)
        glBindVertexArray(VAO)

        # The vbo thing does something
        self.vbo = vbo.VBO(self.verts)  # <- this is where verts is processed

        self.uniformInvT = glGetUniformLocation(self.shader, "invT")

        glBindAttribLocation(self.shader, 0, "position")
        self.position = GLuint(0)
        glBindAttribLocation(self.shader, 1, "color")
        self.color = GLuint(1)
        glBindAttribLocation(self.shader, 2, "vertex_normal")
        self.vertex_normal = GLuint(2)
        glBindAttribLocation(self.shader, 3, "aTexCoord")
        self.texCoord = GLuint(3)

        #self.position = glGetAttribLocation(self.shader, "position")
        #self.color = glGetAttribLocation(self.shader, "color")
        #self.vertex_normal = glGetAttribLocation(self.shader, "vertex_normal")
        #self.texCoord = glGetAttribLocation(self.shader, "aTexCoord")

        self.texUnitUniform = glGetUniformLocation(self.shader, 'texUnit')

        # If necessary, translate shape location based on pos
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

        self.textureGen = self.load_texture()

    def load_texture(self):
        # Load texture image
        try:
            self.textureSurf = Image.open(f"resources/textures/{self.type}_tetris_texture.jpg")
        except Error as e:
            print(f'Major Error: {e}')
            return None

        # Convert data into numpy array
        self.textureData = np.array(list(self.textureSurf.getdata()), np.uint8)

        # Change color format if applicable
        format = GL_RGB if self.textureData.shape[0] == 3 else GL_RGBA

        ### Load Texture Code Initially

        # This is the texture code that initializes the textures.
        
        textureID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, textureID)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        #glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.textureSurf.width, self.textureSurf.height, 0, GL_RGB, GL_UNSIGNED_BYTE, self.textureData)
        glBindTexture(GL_TEXTURE_2D, 0)

        ###

        return textureID

    def Update(self, deltaTime, currentID):
        # TODO
        # If space below block is clear, move downwards one unit
        
        # if (space is clear):
        #     (move down)
        # else:
        #     (indicate a new block must be summoned)      

        pass
        
        # Blocks will not automatically rotate for now
        #if self.id == currentID or currentID == -1:
            # Update Angle if self is a current Shape
            #self.ang += self.rotateSpeed * deltaTime

    def DrawBlock(self):
        ## My Added Texture Code ##
            
        glEnable(GL_TEXTURE_2D)
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.textureGen)

        ##

        ### This is the Professor's code used to render the block with shaders ###
        shaders.glUseProgram(self.shader)
        invT = np.linalg.inv(glGetDouble(GL_MODELVIEW_MATRIX)).transpose()
        glUniformMatrix4fv(self.uniformInvT, 1, False, invT)
        try:
            self.vbo.bind()
            try:
                glEnableVertexAttribArray(self.position)
                glEnableVertexAttribArray(self.color)
                glEnableVertexAttribArray(self.vertex_normal)
                glEnableVertexAttribArray(self.texCoord)
                stride = 44
                glVertexAttribPointer(self.position, 3, GL_FLOAT, False, stride, self.vbo)
                glVertexAttribPointer(self.color, 3, GL_FLOAT, False, stride, self.vbo + 12)
                glVertexAttribPointer(self.vertex_normal, 3, GL_FLOAT, True, stride, self.vbo + 24)
                glVertexAttribPointer(self.texCoord, 2, GL_FLOAT, False, stride, self.vbo + 36)
                glDrawArrays(GL_QUADS, 0, self.model_size)
                
                
            finally:
                self.vbo.unbind()
                glDisableVertexAttribArray(self.position)
                glDisableVertexAttribArray(self.color)
                glDisableVertexAttribArray(self.vertex_normal)
                glDisableVertexAttribArray(self.texCoord)
        finally:
            shaders.glUseProgram(0)
            
           
            glBindTexture(GL_TEXTURE_2D, 0)
            

        ###           
    
    def _delete(self):
        global blockList

        blockList.remove(self)
        del self

    def Render(self):
        m = glGetDouble(GL_MODELVIEW_MATRIX)

        glRotatef(self.ang, *self.axis)

        self.DrawBlock()

        glLoadMatrixf(m)

    ##########################################################
    # Below is the code used before shaders were implemented #
    # In this code, textures did work. Now they do not.      #
    ##########################################################

 #   def OldDrawBlock(self):

        #####################################
        ##        Old Drawing Code         ##
        #####################################

#        global _lightVector

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



import numpy as np
from OpenGL.GL import *
from OpenGL.arrays import vbo
from OpenGL.GL import shaders


class Cube:
    def __init__(self):
        color = np.asfarray([0, 0, 1])

        # 3 positions, 3 colors, 3 normals, 2 UVs
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
                                 ])

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
            vertex_color = vec4(color * min(1, max(0, norm[2])),1.0);
        }""", GL_VERTEX_SHADER)

        self.FRAGMENT_SHADER = shaders.compileShader("""#version 130
        in vec4 vertex_color;
        out vec4 fragColor;
        void main()
        {
        fragColor = vertex_color;
        }""", GL_FRAGMENT_SHADER)

        self.shader = shaders.compileProgram(self.VERTEX_SHADER, self.FRAGMENT_SHADER)
        self.vbo = vbo.VBO(self.verts)

        self.uniformInvT = glGetUniformLocation(self.shader, "invT")
        self.position = glGetAttribLocation(self.shader, "position")
        self.color = glGetAttribLocation(self.shader, "color")
        self.vertex_normal = glGetAttribLocation(self.shader, "vertex_normal")

        self.ang = 0
        self.axis = (3, 1, 1)

    def Update(self, deltaTime):
        pass
        #self.ang += 50.0 * deltaTime

    def DrawBlock(self):
        global _lightVector

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
                glDrawArrays(GL_QUADS, 0, 24)

            finally:
                self.vbo.unbind()
                glDisableVertexAttribArray(self.position)
                glDisableVertexAttribArray(self.color)
                glDisableVertexAttribArray(self.vertex_normal)
        finally:
            shaders.glUseProgram(0)

    def Render(self):
        m = glGetDouble(GL_MODELVIEW_MATRIX)

        #glRotatef(self.ang, *self.axis)

        self.DrawBlock()

        glLoadMatrixf(m)

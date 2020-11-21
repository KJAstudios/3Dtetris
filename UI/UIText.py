# from World.WorldCommon import ScreenSize
import freetype
import glm
from OpenGL.GL import *
from OpenGL.GL import shaders

Characters = dict()


# TODO resources used:
# tutorial: https://learnopengl.com/In-Practice/Text-Rendering
# tutorial code: https://learnopengl.com/code_viewer_gh.php?code=src/7.in_practice/2.text_rendering/text_rendering.cpp
# attempted python implementation: https://stackoverflow.com/questions/63836707/how-to-render-text-with-pyopengl
# pyopenGL documentation: http://pyopengl.sourceforge.net/documentation/manual-3.0/index.html#GL

class Character:

    def __init__(self, texture, glyph):
        self.texture = texture
        self.textureSize = (glyph.bitmap.width, glyph.bitmap.rows)

        if isinstance(glyph, freetype.GlyphSlot):
            self.bearing = (glyph.bitmap_left, glyph.bitmap_top)
            self.advance = glyph.advance.x
        elif isinstance(glyph, freetype.BitmapGlyph):
            self.bearing = (glyph.left, glyph.top)
            self.advance = None
        else:
            raise RuntimeError('unknown glyph type')


class UIText:
    def __init__(self, element):
        self.placeholder = 'Built to avoid errors!'
        self.element = element

    def ProcessEvent(self, event):
        pass


fontfile = "C:\Windows\Fonts\Arial.ttf"


def Init():
    global Characters
    global shader
    face = freetype.Face(fontfile)
    face.set_char_size(48 * 64)
    # load first 128 characters of ASCII set
    for i in range(0, 128):
        face.load_char(chr(i))
        glyph = face.glyph

        # generate texture
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RED, glyph.bitmap.width, glyph.bitmap.rows, 0,
                     GL_RED, GL_UNSIGNED_BYTE, glyph.bitmap.buffer)

        # texture options
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # now store character for later use
        Characters[chr(i)] = Character(texture, glyph)

    glBindTexture(GL_TEXTURE_2D, 0)

    VERTEX_SHADER = shaders.compileShader("""#version 330 core
                        layout (location = 0) in vec4 vertex;
                        out vec2 TexCoords;                
                        uniform mat4 projection;                
                        void main()
                        {
                            gl_Position = projection * vec4(vertex.xy, 0.0, 1.0);
                            TexCoords = vertex.zw;
                        }""", GL_VERTEX_SHADER)

    FRAGMENT_SHADER = shaders.compileShader("""#version 330 core
                        in vec2 TexCoords;
                        out vec4 color;
                        
                        uniform sampler2D text;
                        uniform vec3 textColor;
                        
                        void main()
                        {    
                            vec4 sampled = vec4(1.0, 1.0, 1.0, texture(text, TexCoords).r);
                            color = vec4(textColor, 1.0) * sampled;
                        }""", GL_FRAGMENT_SHADER)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    shader = shaders.compileProgram(VERTEX_SHADER, FRAGMENT_SHADER)


def Render():
    global shader
    projection_matrix = glm.ortho(0.0, 640.0, 0.0, 480.0)
    glUseProgram(shader)
    VAO = GLuint(glGenVertexArrays(1))
    VBO = GLuint(glGenBuffers(1))
    glBindVertexArray(VAO)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, 6 * 4 * 4, None, GL_DYNAMIC_DRAW)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 0, None)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

import numpy as np
import pygame
# from World.WorldCommon import ScreenSize
from UI.UIImage import UIImage
import freetype
from OpenGL.GL import *
from OpenGL.GLU import *

Characters = dict()
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



fontfile="C:\Windows\Fonts\Arial.ttf"
def Init():
    global Characters
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







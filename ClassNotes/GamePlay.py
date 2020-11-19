import pygame
from OpenGL.GL import *
import numpy as np
import math
import random
import ClassNotes.Cube as Cube


def Init():
    global _cube
    global _pos
    _cube = Cube.Cube()
    _pos = np.asfarray([-1, 7, -1])


def ProcessEvent(event):
    return False


def Update(deltaTime):
    global _cube
    global _pos

    _pos[1] -= 1 * deltaTime
    if _pos[1] <= -5:
        _pos[1] = 7

    _cube.Update(deltaTime)


def Render():
    global _cube
    global _pos
    m = glGetDouble(GL_MODELVIEW_MATRIX)
    glTranslatef(*_pos)
    _cube.Render()
    glLoadMatrixf(m)

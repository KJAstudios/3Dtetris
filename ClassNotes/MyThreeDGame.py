import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from SlowCube import SlowCube
from ClassNotes.Cube import Cube as Cube
import ClassNotes.Border as Border
import ClassNotes.GamePlay as GamePlay

# Main Init
pygame.init()
size = width, height = 640, 900
screen = pygame.display.set_mode(size, DOUBLEBUF | OPENGL)

glMatrixMode(GL_PROJECTION)
gluPerspective(45, (width / height), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)

glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)

glTranslate(1.0, 0.0, -20)
glRotate(-15, 0, 1, 0)
glRotate(30, 1, 0, 0)

GamePlay.Init()


def Update(deltaTime):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if GamePlay.ProcessEvent(event):
            continue

    GamePlay.Update(deltaTime)
    return True


def Render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    GamePlay.Render()
    Border.Render()

    pygame.display.flip()


_gTickLastFrame = pygame.time.get_ticks()
_gDeltaTime = 0.0
while Update(_gDeltaTime):
    Render()
    t = pygame.time.get_ticks()
    _gDeltaTime = (t - _gTickLastFrame) / 1000.0
    _gTickLastFrame = t

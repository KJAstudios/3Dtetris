import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()
size = width, height = 640, 480
screen = pygame.display.set_mode(size, DOUBLEBUF | OPENGL)

gluPerspective(45, (width / height), 0.1, 50.0)

glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)
glTranslate(0.0, 0.0, -5)

verts = ((1, -1, -1),
         (1, 1, -1),
         (-1, 1, -1),
         (-1, -1, -1),
         (1, -1, 1),
         (1, 1, 1),
         (-1, -1, 1),
         (-1, 1, 1))

surfaces = ((0, 1, 2, 3),
            (3, 2, 7, 6),
            (6, 7, 5, 4),
            (4, 5, 1, 0),
            (1, 5, 7, 2),
            (4, 0, 3, 6))

colors = ((0, 0, 1),
          (0, 1, 0),
          (0, 0, 1),
          (0, 1, 0))

ang = 0

clock = pygame.time.Clock()
gameQuit = False
while not gameQuit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameQuit = True

    deltaTime = float(clock.tick(60)) / 1000

    ang += 50.0 * deltaTime

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    m = glGetDouble(GL_MODELVIEW_MATRIX)

    glRotatef(ang, 3, 1, 1)
    glBegin(GL_QUADS)
    for surface in surfaces:
        for i, vert in enumerate(surface):
            glColor3fv(colors[i])
            glVertex3fv(verts[vert])
    glEnd()

    glLoadMatrixf(m)

    pygame.display.flip()


import random

import pygame
from pygame.locals import *

import Border
from Cube import Cube
from gamecommon import *

# Main Init
pygame.init()
size = width, height = 640, 480

pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_COMPATIBILITY)

screen = pygame.display.set_mode(size, DOUBLEBUF | OPENGL)

pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)

glMatrixMode(GL_PROJECTION)
gluPerspective(45, (width / height), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)

glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)

glTranslate(0.0, 0, -30.0)
glRotate(-15, 0, 1, 0)
# glRotate(-7, 0, 0, 1)
# glRotate(-35, 1, 0, 0)

random.seed()


def AddBlockToGame(type, pos):
    blockList.append(Cube(type, pos))
    blockList[-1].fadeIn = True

AddBlockToGame(type=shapeList[random.randint(0, 4)], pos=[0, 9, 0])

# import UI
from UI.UIText import UIText

text = UIText()
text.Init()

currentShapeID = -1


def Update(deltaTime):
    global currentShapeID
    global gameState

    if len(blockList) == 0:
        AddBlockToGame(type=shapeList[random.randint(0, 4)], pos=[0, 9, 0])

    # If the game is paused,
    if gameState[0] == 1:
        for block in blockList:
            block.fadeOut = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        for cube in blockList:
            cube.ProcessEvent(event)
        # if UI.ProcessEvent(event) == True:
        #    continue

    for id, block in enumerate(blockList):
        if block.doesExist():
            # id can be used to determine if a block should be able to be rotated
            block.Update(deltaTime, currentShapeID)
        else:
            del blockList[id]
    return True


def Render(screen):
    global text
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)


    for block in blockList:
        if block.doesExist():
            block.Render()
    Border.Render()
    color = (255, 0, 0)
    rtext = 'Hello World'
    text.Render(screen, rtext, 20, 50, 1, color)

    # image = pygame.image.load("Data/GreenBar.png")
    # UIImage(image)

    pygame.display.flip()


_gTickLastFrame = pygame.time.get_ticks()
_gDeltaTime = 0.0

while Update(_gDeltaTime):
    Render(screen)
    t = pygame.time.get_ticks()
    _gDeltaTime = (t - _gTickLastFrame) / 1000.0
    _gTickLastFrame = t

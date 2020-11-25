import pygame
from pygame.locals import *
from gamecommon import *
from Cube import Cube

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

glTranslate(0.0, 0.0, -15)

blockList.append(Cube(type="box", pos=(-5, 3, 0)))
blockList.append(Cube(type="T", rotateSpeed=-150.0, pos=(0, 3, 0)))
blockList.append(Cube(type="S", rotateSpeed=175.0, pos=(5, 3, 0)))
blockList.append(Cube(type="straight", rotateSpeed=125.0, pos=(-5, -3, 0)))
blockList.append(Cube(type="L", rotateSpeed=-125.0, pos=(0, -3, 0)))

# import UI
from UI.UIText import UIText

text = UIText()
text.Init()

currentShapeID = -1


def Update(deltaTime):
    global currentShapeID

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                currentShapeID = 0
            elif event.key == pygame.K_2:
                currentShapeID = 1
            elif event.key == pygame.K_3:
                currentShapeID = 2
            elif event.key == pygame.K_4:
                currentShapeID = 3
            elif event.key == pygame.K_5:
                currentShapeID = 4
            elif event.key == pygame.K_6:
                currentShapeID = 5
            elif event.key == pygame.K_7:
                currentShapeID = -1
        #if UI.ProcessEvent(event) == True:
            continue

    for id, block in enumerate(blockList):
        # id can be used to determine if a block should be able to be rotated
        block.Update(deltaTime, currentShapeID)

    # UI.Update(deltaTime)

    return True


def Render(screen):
    global text
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    for block in blockList:
        block.Render()
    color = (255,100,100)
    rtext = 'hello world'
    text.Render(screen, rtext, 20, 50, 1, color)

    #instructions = 'Press num keys to switch blocks'
    #text.Render(screen, instructions, 10, 620, 0.5, color)

    pygame.display.flip()


_gTickLastFrame = pygame.time.get_ticks()
_gDeltaTime = 0.0
timer = 0
while Update(_gDeltaTime):
    Render(screen)
    t = pygame.time.get_ticks()
    _gDeltaTime = (t - _gTickLastFrame) / 1000.0
    _gTickLastFrame = t
    timer += 1
    #if timer > 50:
    #    blockList[1]._delete()
    #    timer = 0

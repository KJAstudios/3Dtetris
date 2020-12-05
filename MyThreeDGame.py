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

glTranslate(0.0, -7.0, -35.0)
glRotate(-15, 0, 1, 0)
glRotate(-7, 0, 0, 1)
glRotate(-35, 1, 0, 0)


def AddBlockToGame(type, pos, rotateSpeed = 100):
    blockList.append(Cube(type, rotateSpeed, pos))
    blockList[-1].fadeIn = True


AddBlockToGame(type="box", pos=[0, 0, 9])
AddBlockToGame(type="T", rotateSpeed=-150.0, pos=[1, 1, 9])
AddBlockToGame(type="S", rotateSpeed=175.0, pos=[-2, 0, 9])
AddBlockToGame(type="straight", rotateSpeed=125.0, pos=[-2, 2, 9])
AddBlockToGame(type="L", rotateSpeed=-125.0, pos=[0, 2, 9])



# import UI
from UI.UIText import UIText

text = UIText()
text.Init()

currentShapeID = -1

def Update(deltaTime):
    global currentShapeID
    global gameState

    # If the game is paused,
    if gameState[0] == 1:
        for block in blockList:
            block.fadeOut = True

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
        for cube in blockList:
            cube.ProcessEvent(event)
        #if UI.ProcessEvent(event) == True:
        #    continue

    for id, block in enumerate(blockList):
        # id can be used to determine if a block should be able to be rotated
        block.Update(deltaTime, currentShapeID)

        #if id == 0:
        #    block.newAlpha -= deltaTime

        #if block.newAlpha <= 0:
        #    block._delete()



    # UI.Update(deltaTime)

    return True


def Render(screen):
    global text
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    for block in blockList:
        block.Render()
    color = (255, 0, 0)
    rtext = 'hello world'
    text.Render(screen, rtext, 20, 50, 1, color)



    #instructions = 'Press num keys to switch blocks'
    #text.Render(screen, instructions, 10, 620, 0.5, color)

    pygame.display.flip()


_gTickLastFrame = pygame.time.get_ticks()
_gDeltaTime = 0.0
timer = 0  # Timer for testing different mechanics

while Update(_gDeltaTime):
    Render(screen)
    t = pygame.time.get_ticks()
    _gDeltaTime = (t - _gTickLastFrame) / 1000.0
    _gTickLastFrame = t
    timer += 1



    if timer > 55:
        # if blockList[0].pos[2] != 0:
        #     blockList[0].pos[2] += -1
        timer = 0


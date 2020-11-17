import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from SlowCube import SlowCube

# Main Init
pygame.init()
size = width, height = 640, 480
screen = pygame.display.set_mode(size, DOUBLEBUF | OPENGL)

glMatrixMode(GL_PROJECTION)
gluPerspective(45, (width / height), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)

glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LESS)

glTranslate(0.0, 0.0, -15)

blockList = []

blockList.append(SlowCube(len(blockList),type="box",pos=(-5,3,0)))
blockList.append(SlowCube(len(blockList),type="T",rotateSpeed=-150.0,pos=(0,3,0)))
blockList.append(SlowCube(len(blockList),type="S",rotateSpeed=175.0,pos=(5,3,0)))
blockList.append(SlowCube(len(blockList),type="straight",rotateSpeed=125.0,pos=(-5,-3,0)))
blockList.append(SlowCube(len(blockList),type="L",rotateSpeed=-125.0,pos=(0,-3,0)))


currentShapeID = 0

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
                
    for id, block in enumerate(blockList):
        # id can be used to determine if a block should be able to be rotated
        block.Update(deltaTime,currentShapeID)

    return True


def Render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    for block in blockList:
        block.Render()

    pygame.display.flip()


_gTickLastFrame = pygame.time.get_ticks()
_gDeltaTime = 0.0
while Update(_gDeltaTime):
    Render()
    t = pygame.time.get_ticks()
    _gDeltaTime = (t - _gTickLastFrame) / 1000.0
    _gTickLastFrame = t

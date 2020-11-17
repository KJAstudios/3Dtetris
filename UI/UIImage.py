import numpy as np
import pygame



class UIImage():

    def __init__(self, element=None):
        if element != None:
            self.path = element.get("path", None)
            if self.path == None:
                self.surf = None
            else:
                self.surf = pygame.image.load(self.path)
            self.x = int(element.get("x", 0))
            self.y = int(element.get("y", 0))
            self.width = int(element.get("width", 0))
            self.height = int(element.get("height", 0))
            if self.surf != None:
                self.surf = pygame.transform.scale(self.surf, (self.width, self.height))
            self.rect = pygame.Rect((self.x, self.y), (self.width, self.height))
            self.justify = element.get("justify", "left")
            self.vjustify = element.get("vjustify", "top")
            anchor = element.find("Anchor")

            if anchor != None:
                self.anchorX = float(anchor.get("x", 0))
                self.anchorY = float(anchor.get("y", 0))

            else:
                self.anchorX = 0
                self.anchorY = 0
            v = self.visible = element.get("visible", 'false')
            self.visible = v == 'true'
            self._CalcRect()
        else:
            self.x = None
            self.y = None
            self.width = None
            self.height = None
            self.surf = None
            self.visible = True

    def _CalcRect(self):
        self.rect.left = self.anchorX * 640 + self.x
        if self.justify == "right":
            self.rect.left -= self.width
        if self.justify == "center":
            self.rect.left -= self.width // 2

        self.rect.top = self.anchorY * 480 + self.y

        if self.justify == "bottom":
            self.rect.left -= self.height
        if self.justify == "center":
            self.rect.top -= self.height // 2

        self.rect.width = self.width
        self.rect.height = self.height

    def ProcessEvent(self, event):
        return False

    def Update(self, deltaTime):
        pass

    def Render(self, screen):
        if self.visible and self.surf != None:
            screen.blit(self.surf, self.rect)


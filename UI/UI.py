import pygame
import xml.etree.ElementTree as ET
from UI.UIImage import UIImage
from UI.UIText import UIText

_uiObjects = []

def Init():
    global _uiObjects
    # global _uiIds

    tree = ET.parse("Data/UI.xml")
    root = tree.getroot()  # root is UI element
    groups = root.find("Group")

    if groups != None:
        for element in groups.findall("*"):
            if element.tag == "Image":
                img = UIImage(element)
                _uiObjects.append(img)
            elif element.tag == "Text":
                img = UIText(element)
                _uiObjects.append(img)
            # elif element.tag == "Button":
            #     img = UIButton(element)
            #     _uiObjects.append(img)

            # if img != None:
            #     id = element.get('id')
            #     if id != None:
            #         _uiIds[id] = img
    for i in _uiObjects:
        print(i)

def ProcessEvent(event):
    global _uiObjects

    for i in reversed(_uiObjects):
        if i.ProcessEvent(event) == True:
            return True

    return False

def Update(deltaTime):
    global _uiObjects


    for i in _uiObjects:
        i.Update(deltaTime)

def Render(screen):
    global _uiObjects

    for i in _uiObjects:
        i.Render(screen)


def CleanUp():
    pass
import pygame, tkinter
from tkinter import filedialog

pygame.font.init()
font = pygame.font.Font(None, 20)

def file_prompt():
    tkinter.Tk().withdraw()
    fn = filedialog.askopenfilename()
    return open(fn)

class Button:
    def __init__(self, dimensions, color, text=None):
        self.rect  = pygame.Rect(0, 0, dimensions[0], dimensions[1])
        self.color = color
        self.text  = text
    def draw(self, target_surface, x=None, y=None):
        self.rect.centerx = x if x != None else self.rect.centerx
        self.rect.centery = y if y != None else self.rect.centery

        text_surface = font.render(self.text, True, "black")

        pygame.draw.rect(target_surface, self.color, self.rect)
        target_surface.blit(text_surface, (self.rect.centerx - text_surface.get_width()/2, self.rect.centery - text_surface.get_height()/2))    

class Title:
    pass

class InputBox:
    pass

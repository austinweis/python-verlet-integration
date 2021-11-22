from tkinter.constants import NUMERIC
import pygame, tkinter
from tkinter import filedialog

pygame.font.init()
font = pygame.font.Font(None, 20)

def file_prompt():
    tkinter.Tk().withdraw()
    path = filedialog.askopenfilename()
    return path

class Button:
    def __init__(self, dimensions, color, text=''):
        self.rect  = pygame.Rect(0, 0, dimensions[0], dimensions[1])
        self.color = color
        self.text  = text
    def draw(self, target_surface, x=0, y=0):
        self.rect.centerx = x
        self.rect.centery = y

        text_surface = font.render(self.text, True, "black")

        pygame.draw.rect(target_surface, self.color, self.rect)
        target_surface.blit(text_surface, (self.rect.centerx - text_surface.get_width()/2, self.rect.centery - text_surface.get_height()/2))    

class Title:
    def __init__(self, color, text=''):
        self.color = color
        self.text  = text
    def draw(self, target_surface, x=0, y=0):
        text_surface = font.render(self.text, True, self.color)

        target_surface.blit(text_surface, (x - text_surface.get_width()/2, y - text_surface.get_height()/2))    


class InputBox:
    def __init__(self, dimensions, color, text='', numeric=False):
        self.rect = pygame.Rect(0, 0, dimensions[0], dimensions[1])
        self.color = color
        self.text = text
        self.text_surface = font.render(text, True, self.color)
        self.active = False
        self.numeric = numeric

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if self.numeric:
                        self.text += event.unicode
                        try:       
                            self.text = str(float(self.text))
                        except:
                            self.text = self.text[:-1]
                            self.text = self.text
                    else:
                        self.text += event.unicode
                self.text_surface = font.render(self.text, True, self.color)

    def draw(self, target_surface, x=0, y=0):
        self.rect.centerx = x
        self.rect.centery = y

        target_surface.blit(self.text_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(target_surface, self.color, self.rect, 2)

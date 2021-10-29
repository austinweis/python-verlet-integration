import math, json, os

import pygame
import rag
import editor
import tkinter as tk
from tkinter.filedialog import askopenfilename

pygame.init()

def main():
    # window properties
    width, height = 1280, 720
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Verlet Physics Simulation")
    screen_color = (25, 25, 25)
    screen.fill(screen_color)
    font = pygame.font.Font(None, 20)

    clock = pygame.time.Clock()
    scale = 20

    #menu bar setup
    menuBarHeight = 20
    menuBar = pygame.Rect((0, 0),(1280, menuBarHeight))
    menuBarColor = (120, 120, 120)

    #edit button
    editButton = pygame.Rect((0,0), (50, menuBarHeight))
    editButtonColor = (200,200,200)
    editButtonText = "Editor"

    # load ragdoll from json
    #data = open(os.path.dirname(os.path.realpath(__file__)) + "/object.rag", "r")
    tk.Tk().withdraw() # part of the import if you are not using other tkinter functions
    fn = askopenfilename()
    data = open(fn)
    data = json.loads(data.read())
    ragdoll = rag.Rag(data)

    mouse_point = None # point following mouse

    point_radius, stick_width = 5, 3

    def update_rag(rag, rigidity):
        rag.move_dynamic_points()
        for i in range(rigidity):
            rag.update_sticks()
            rag.constrain_points((width/scale, height/scale))

    def draw_rag(rag):
        color = (255, 255, 255)
        for s in rag.sticks:
            p0 = rag.points[s[0]]
            p1 = rag.points[s[1]]
            pygame.draw.line(screen, color, (p0[0] * scale, p0[1] * scale), (p1[0] * scale, p1[1] * scale), stick_width)
        for i, p in enumerate(rag.points):
            if i in rag.statics:
                color = (255, 0, 0)
            else:
                color = (255, 255, 255)
            pygame.draw.circle(screen, color, (p[0] * scale, p[1] * scale), point_radius)


    running = True
    while running:
        m_x = pygame.mouse.get_pos()[0] # get x value of mouse position
        m_y = pygame.mouse.get_pos()[1] # get y value of mouse position

        #gui
        screen.fill(screen_color)
        update_rag(ragdoll, 6)
        draw_rag(ragdoll)
        pygame.draw.rect(screen, menuBarColor, menuBar)
        textSurface = font.render(editButtonText, True, (0, 0, 0))
        pygame.draw.rect(screen, editButtonColor, editButton)
        screen.blit(textSurface, (editButton.centerx - textSurface.get_width()/2, editButton.centery - textSurface.get_height()/2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, p in enumerate(ragdoll.points):
                    if round(p[0]) == round(m_x/scale) and round(p[1]) == round(m_y/scale):
                        mouse_point = i
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_point = None
                if event.button == pygame.BUTTON_LEFT:
                    if editButton.collidepoint(m_x, m_y):
                        editor.edit()
                        pygame.quit()
                        exit()

        if mouse_point in ragdoll.statics:
            ragdoll.move_static_point(mouse_point, (m_x/scale, m_y/scale))
        elif mouse_point != None:
            ragdoll.points[mouse_point] = [m_x/scale, m_y/scale] * 2
            
        pygame.display.update()
        clock.tick(60)
        
if __name__ == '__main__':
    print("Running")
    main()
   

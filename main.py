import pygame
import math
import json
import os
from classes import *

pygame.init()

def main():
    width, height = 1280, 720
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Verlet Physics Simulation")
    screenColor = (25, 25, 25)
    screen.fill(screenColor)
    clock = pygame.time.Clock()
    cellSize = 20

    data = open(os.path.dirname(os.path.realpath(__file__)) + "/object.rag", "r")
    data = json.loads(data.read())

    renderForm = False

    cursorPoint = None

    points = []
    sticks = []
    forms  = []
    
    for i in range(len(data["points"])):
        _engine = False
        for e in data["properties"]["static"]:
            if e == i:
                points.append(Engine((data["points"][i][0]*cellSize, data["points"][i][1]*cellSize)))
                _engine = True
        for e in data["properties"]["follow_mouse"]:
            if e == i:
                points.append(Engine((data["points"][i][0]*cellSize, data["points"][i][1]*cellSize), True))
                _engine = True
        if _engine == False:
            points.append(Point((data["points"][i][0]*cellSize, data["points"][i][1]*cellSize), (data["points"][i][0]*cellSize, data["points"][i][1]*cellSize)))
    for s in data["sticks"]:
        sticks.append(Stick(points[s[0]], points[s[1]]))
    path = []
    for f in data["forms"]:
        path.append(points[f[0]])
        path.append(points[f[1]])
    forms.append(Form(path))

    for p in points:
        if type(p) == Engine:
            if p.followCursor:
                cursorPoint = p

    print(sticks[0].length)

    RIGIDITY = 6
    INERTIA = 0.99
    BOUNCE = 1
    GRAVITY = 1

    def updatePoints():
        for p in points:
            if type(p) == Point:
                vx = (p.x - p.ox) * INERTIA
                vy = (p.y - p.oy) * INERTIA

                p.ox = p.x
                p.oy = p.y

                p.x += vx
                p.y += vy

                p.y += GRAVITY
            elif type(p) == Engine:
                if cursorPoint != None:
                    p.x, p.y = pygame.mouse.get_pos()[0] - (cursorPoint.offset[0] - p.offset[0]), pygame.mouse.get_pos()[1] - (cursorPoint.offset[1] - p.offset[1])
                    if cursorPoint == p: 
                        p.x, p.y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
                    

    def updateSticks():
        for s in sticks:
            dx = s.p1.x - s.p0.x
            dy = s.p1.y - s.p0.y
            distance = math.sqrt(dx * dx + dy * dy)
            difference = s.length - distance
            percent = difference/distance/2
            offsetX = dx * percent
            offsetY = dy * percent

            if type(s.p0) == Point:
                s.p0.x -= offsetX
                s.p0.y -= offsetY
            if type(s.p1) == Point:
                s.p1.x += offsetX
                s.p1.y += offsetY 

    def constrainPoints():
        for p in points:
            if type(p) == Point:
                vx = (p.x - p.ox) * INERTIA
                vy = (p.y - p.oy) * INERTIA

                if p.x > width:
                    p.x = width
                    p.ox = p.x + vx * BOUNCE
                if p.x < 0:
                    p.x = 0
                    p.ox = p.x + vx * BOUNCE
                if p.y > height:
                    p.y = height
                    p.oy = p.y + vy * BOUNCE
                if p.y < 0:
                    p.y = 0
                    p.oy = p.y + vy * BOUNCE

    def displayUpdate():
        screen.fill(screenColor)

        # Render forms
        if renderForm:
            for f in forms:
                polygonPath = []
                for p in f.path:
                    polygonPath.append((p.x, p.y))
                if len(polygonPath) > 2:
                    pygame.draw.polygon(screen, (255, 255, 255), polygonPath)
        else:
        # Render sticks
            for s in sticks:     
                pygame.draw.line(screen, s.color, (s.p0.x, s.p0.y),(s.p1.x, s.p1.y), width=s.thickness)

            # Render points
            for p in points:
                pygame.draw.circle(screen, p.color, (p.x, p.y), p.size) 

        screen.blit(screen, (0, 0))
        pygame.display.update()

    running = True

    while running:
        updatePoints()
        for i in range(RIGIDITY):
            updateSticks()
            constrainPoints()
        displayUpdate()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    renderForm = not renderForm

        clock.tick(60)

if __name__ == '__main__':
    main()